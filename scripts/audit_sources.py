"""Read-only live catalog audit. Requires requests and PyYAML; no credentials used."""
import concurrent.futures as futures
import collections
import csv
import datetime
import hashlib
import json
import re
import threading
import time
import sys
from pathlib import Path
from urllib.parse import urlsplit
import requests
import yaml

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs' / 'sources-audit'
LIMIT = 262144
LOCKS = collections.defaultdict(threading.Lock)

def inventory(s):
    entries = [('base_url', s['base_url'])] if s.get('base_url') else []
    entries += list(s.get('endpoints', {}).items())
    entries += [('dataset:' + str(x.get('partition') or i), x['url']) for i, x in enumerate(s.get('dataset', {}).get('sources', []))]
    seen = set()
    for label, url in entries:
        if url not in seen:
            seen.add(url)
            yield dict(source=s['id'], label=label, catalog_url=url, url=url, protocol=s.get('protocol'), dataset=label.startswith('dataset:'))

def fields(value, path='$', result=None):
    result = {} if result is None else result
    result.setdefault(path, set()).add(type(value).__name__)
    if isinstance(value, dict):
        for k, v in value.items():
            fields(v, path + '.' + k, result)
    elif isinstance(value, list):
        for v in value:
            fields(v, path + '[]', result)
    return {k: sorted(v) for k, v in result.items()}

def probe(item):
    r = dict(item, checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(), status=None, bytes_read=0)
    url = item['url']
    if '{' in url:
        url = url.replace('{ano}', '2023').replace('{etapa}', 'anos_iniciais')
        r['url'] = url
        r['parameters_note'] = 'Template example: ano=2023, etapa=anos_iniciais; other values untested'
    if '{' in url or not url.startswith(('http://', 'https://')):
        return dict(r, outcome='unresolved URL template')
    start = time.monotonic()
    try:
        with LOCKS[urlsplit(url).netloc]:
            with requests.get(url, headers={'User-Agent': 'farol-source-audit/1.0', 'Accept': '*/*', 'Accept-Encoding': 'identity'}, timeout=(10, 20), stream=True) as response:
                r.update(status=response.status_code, final_url=response.url, content_type=response.headers.get('Content-Type'), content_length=response.headers.get('Content-Length'), content_range=response.headers.get('Content-Range'))
                body = bytearray()
                exhausted = True
                for chunk in response.iter_content(8192):
                    body.extend(chunk)
                    if len(body) > LIMIT or time.monotonic() - start > 35:
                        exhausted = False
                        break
                r['bytes_read'] = len(body)
                r['complete'] = exhausted
                r['sha256_sample'] = hashlib.sha256(body).hexdigest()
                decoded = body.decode('utf-8-sig', errors='replace')
                r['preview'] = decoded[:500] if not body.startswith(b'PK') else 'ZIP archive (PK signature); members/schema not verified'
                kind = 'text'
                try:
                    value = json.loads(decoded) if r['complete'] else None
                    if value is not None:
                        kind = 'json'
                        r['observed_fields'] = fields(value)
                        r['array_counts'] = {}
                        def counts(v, p='$'):
                            if isinstance(v, list):
                                r['array_counts'][p] = len(v)
                            elif isinstance(v, dict):
                                for k, x in v.items(): counts(x, p + '.' + k)
                        counts(value)
                        r['reported_totals'] = {}
                        def totals(v, p='$'):
                            if isinstance(v, dict):
                                for k, x in v.items():
                                    if k.lower() in ('total', 'count', 'totalregistros', 'totalelements', 'total_count') and isinstance(x, (int, float)):
                                        r['reported_totals'][p + '.' + k] = x
                                    if isinstance(x, dict): totals(x, p + '.' + k)
                        totals(value)
                        if isinstance(value, dict) and (value.get('success') is False or value.get('error')):
                            r['application_error'] = True
                except (ValueError, RecursionError):
                    pass
                if body.startswith(b'PK'): kind = 'zip'
                elif '<html' in decoded[:2000].lower() or '<!doctype html' in decoded[:2000].lower(): kind = 'html'
                elif decoded.lstrip().startswith('<?xml') or '<rss' in decoded[:1000]: kind = 'xml'
                elif '.csv' in url.lower() and kind == 'text':
                    kind = 'csv'
                    r['observed_csv_header'] = next(csv.reader([decoded.splitlines()[0]], delimiter=';'), []) if decoded else []
                r['body_kind'] = kind
                code = response.status_code
                r['outcome'] = ('auth/access blocked' if code in (401,403) else 'rate limited' if code == 429 else 'HTTP error' if code >= 400 else 'application error' if r.get('application_error') else 'HTML returned; data unverified' if kind == 'html' and 'html' not in (item.get('protocol') or '') else 'response received')
    except requests.RequestException as exc:
        r.update(outcome='connection/TLS/timeout failure', error=str(exc))
    r['elapsed_s'] = round(time.monotonic() - start, 3)
    return r

def cell(v):
    return str(v if v is not None else 'unknown').replace('|', '\\|').replace('\n', ' ').replace('\r', '')

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    catalog = yaml.safe_load((ROOT / 'docs/sources.yaml').read_text(encoding='utf-8'))
    items = [x for s in catalog['sources'] for x in inventory(s)]
    # Additional usable resource queries; original catalog URLs remain independently tested.
    for s in catalog['sources']:
        base = s.get('base_url', '')
        url = None
        if 'ckan' in s.get('protocol', ''):
            bases = [u for u in s.get('endpoints', {}).values() if u.endswith('/action')]
            if bases: url = bases[0] + '/package_search?rows=1'
        if s['id'] == 'bacen': url = base + '.11/dados/ultimos/1?formato=json'
        if s['id'] == 'ibge': url = base + '/v1/localidades/estados'
        if s['id'] == 'siconfi': url = base + '/entes'
        if s['id'] == 'opensky': url = base + '/states/all?lamin=-24&lomin=-47&lamax=-23&lomax=-46'
        if url: items.append(dict(source=s['id'],label='representative query',catalog_url=base,url=url,protocol=s.get('protocol'),dataset=False))
    results = []
    if '--render' in sys.argv:
        results = [json.loads(x) for x in (OUT / 'results.jsonl').read_text(encoding='utf-8').splitlines()]
    else:
        with (OUT / 'results.jsonl').open('w', encoding='utf-8') as log, futures.ThreadPoolExecutor(max_workers=16) as pool:
            for r in pool.map(probe, items):
                results.append(r)
                log.write(json.dumps(r, ensure_ascii=False) + '\n'); log.flush()
                print('{} {} {}'.format(len(results), r['source'], r['outcome']), flush=True)
    (OUT / 'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
    md = ['# Live source audit', '', 'Run: ' + datetime.datetime.now(datetime.timezone.utc).isoformat(), '',
          'Read-only GET probes, TLS verification enabled, no credentials. Every unique catalog URL per source is tested, including base URLs and all dataset partitions. Template examples use 2023 / anos_iniciais. A base URL error does not prove its API is down. HTTP 2xx confirms a response, not all client operations. Missing parameters, authentication, HTML login/challenge pages and network failures remain unverified.', '',
          'Load = bytes of response body read (HTTP framing/TLS excluded); capped near 256 KiB per request. Content-Length is server-reported representation size, not database size. API-wide totals are unknown unless explicitly reported. Catalog MB estimates are unverified and separate from measured bytes. No full dataset ingestion, archive member verification, pagination crawl or load/stress test was performed. Observed fields cover complete JSON responses only; catalog fields are declared client models, not verified upstream fields. Seconds include waiting for the per-host request lock and are not pure server latency. Bodies are sampled; previews are limited to 500 characters. CSV headers are observed, but row totals are unknown for truncated files. Network/TLS failures describe this test environment, not confirmed global outages.', '',
          'Machine-readable endpoint evidence: [results.json](results.json). Declared client contracts: [declared-contracts.json](declared-contracts.json).', '',
          '## Source summary', '', '| Source | Data described in catalog | HTTP reached / probes | Successful responses* | Outcomes | Probe bytes | Known dataset file bytes (sized / listed) | Catalog dataset estimate MB |', '|---|---|---:|---:|---|---:|---|---:|']
    for s in catalog['sources']:
        rows = [r for r in results if r['source']==s['id']]
        datasets = [r for r in rows if r['dataset']]
        sized = [r for r in datasets if r['outcome']=='response received' and r.get('content_length')]
        load = '{} bytes ({}/{})'.format(sum(int(r['content_length']) for r in sized),len(sized),len(datasets)) if datasets else 'N/A; API total unknown'
        md.append('| ' + ' | '.join(map(cell,[s['id'],s.get('description',''),str(sum(r['status'] is not None for r in rows))+'/'+str(len(rows)),sum(r['outcome']=='response received' for r in rows),dict(collections.Counter(r['outcome'] for r in rows)) if rows else 'N/A: no upstream URL',sum(r['bytes_read'] for r in rows),load,s.get('dataset',{}).get('approx_size_mb')])) + ' |')
    md += ['', '*Successful responses means HTTP success without a detected JSON error or unexpected HTML. This includes service metadata and intentionally scraped HTML, and does not prove every operation works. A partial dataset byte sum is a lower bound, not its total load.', '']
    md += ['', '## Endpoint results', '', '| Source / endpoint | Requested URL | HTTP / outcome | Format | Bytes read | Complete body | Server Content-Length | Seconds | Exact observed fields / counts |', '|---|---|---|---|---:|---|---:|---:|---|']
    for r in results:
        observed = r.get('observed_fields') or r.get('observed_csv_header') or r.get('preview') or r.get('error','')
        md.append('| ' + ' | '.join(map(cell,[r['source']+' / '+r['label'],r['url'],str(r['status'])+' / '+r['outcome'],r.get('body_kind'),r['bytes_read'],r.get('complete'),r.get('content_length'),r.get('elapsed_s'),str(observed)+'; arrays='+str(r.get('array_counts',{}))+'; reported totals='+str(r.get('reported_totals',{}))])) + ' |')
    (OUT / 'declared-contracts.json').write_text(json.dumps({s['id']:s.get('returned_fields',{}) for s in catalog['sources']},ensure_ascii=False,indent=2),encoding='utf-8')
    (OUT / 'report.md').write_text('\n'.join(md),encoding='utf-8')
    print(json.dumps(dict(collections.Counter(r['outcome'] for r in results))))

if __name__ == '__main__':
    main()
