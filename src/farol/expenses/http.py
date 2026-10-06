"""Bounded requests with pagination and same-origin credential isolation."""
import json
import re
import time
from decimal import Decimal
from urllib.parse import urljoin, urlsplit

import requests

from .contracts import ContractError, digest


def records_from(value, path):
    if isinstance(value, dict) and (value.get('success') is False or value.get('error')):
        raise ContractError('Upstream application error')
    for key in (path or '').split('.'):
        if key:
            if not isinstance(value, dict) or key not in value:
                raise ContractError('Expected record envelope missing')
            value = value[key]
    if not isinstance(value, list) or any(not isinstance(x, dict) for x in value):
        raise ContractError('Expected array of record objects')
    return value


def fetch(url, params, headers, cfg, session=None):
    session = session or requests.Session()
    for attempt in range(3):
        response = session.get(url, params=params, headers=headers, timeout=(10, cfg['timeout_s']),
                               stream=True, allow_redirects=False)
        with response:
            body = bytearray()
            for chunk in response.iter_content(65536):
                body.extend(chunk)
                if len(body) > cfg['max_page_bytes']:
                    raise ContractError('Response exceeds configured body limit')
            if response.status_code in (429, 500, 502, 503, 504) and attempt < 2:
                delay = response.headers.get('Retry-After', '')
                if delay.isdigit() and int(delay) > 60:
                    raise ContractError('Server Retry-After exceeds run retry budget')
                time.sleep(int(delay) if delay.isdigit() else 2 ** (attempt + 1))
                continue
            # The caller persists even HTTP/application failures before parsing.
            return response.status_code, response.headers.get('Content-Type', ''), bytes(body)
    raise ContractError('Retry budget exhausted')


def next_request(value, rows, url, params, cfg):
    mode = cfg['pagination']
    if mode == 'single':
        if isinstance(value, dict) and isinstance(value.get('resposta'), dict):
            metadata = value['resposta']
            if metadata.get('status') != 'OK':
                raise ContractError('TCE-PE application status is not OK')
            if int(metadata.get('tamanhoResultado', len(rows))) != len(rows):
                raise ContractError('TCE-PE result count mismatch')
            if len(rows) >= int(metadata.get('limiteResultado', len(rows) + 1)):
                raise ContractError('TCE-PE response reached result cap')
        return None
    if mode == 'empty_page':
        if not rows:
            return None
        p = dict(params)
        key = cfg['page_param']
        p[key] = int(p.get(key, 1)) + 1
        return url, p
    if mode == 'links':
        links = [x['href'] for x in value.get('links', []) if x.get('rel') == 'next']
        if not links:
            if value.get('hasMore') is True:
                raise ContractError('hasMore without a next link')
            return None
        target = urljoin(url, links[0])
        if urlsplit(target)[:2] != urlsplit(cfg['url'])[:2]:
            raise ContractError('Cross-origin pagination rejected')
        return target, {}
    raise ContractError('Unknown pagination contract')


def extract(cfg, headers, load_page, save_page, session=None):
    url, params = cfg['url'], dict(cfg.get('params', {}))
    result, seen_requests, seen_bodies = [], set(), set()
    for page in range(1, cfg['max_pages'] + 1):
        request_hash = digest([url, params])
        if request_hash in seen_requests:
            raise ContractError('Repeated pagination request')
        seen_requests.add(request_hash)
        cached = load_page(page, request_hash)
        if cached is None:
            time.sleep(cfg['request_interval_s'])
            status, content_type, body = fetch(url, params, headers, cfg, session=session)
            save_page(page, request_hash, status, content_type, body, url, params)
        else:
            status, content_type, body = cached
        if status != 200:
            raise ContractError(f'HTTP {status}; data not published')
        try:
            declared = re.search(r'charset\s*=\s*["\']?([^;"\'\s]+)', content_type, re.I)
            value = json.loads(body.decode(declared.group(1) if declared else 'utf-8-sig'), parse_float=Decimal)
        except (ValueError, UnicodeDecodeError, LookupError):
            raise ContractError('Response is not JSON') from None
        rows = records_from(value, cfg.get('records'))
        fingerprint = digest(rows)
        if rows and fingerprint in seen_bodies:
            raise ContractError('Repeated data page')
        if rows:
            seen_bodies.add(fingerprint)
        result.extend((page, i, x) for i, x in enumerate(rows))
        subsequent = next_request(value, rows, url, params, cfg)
        if subsequent is None:
            return result
        url, params = subsequent
    raise ContractError('Page cap reached; incomplete partition')
