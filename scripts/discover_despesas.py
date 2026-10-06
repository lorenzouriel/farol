"""Bounded contract discovery; credentials and response values stay out of stdout."""
import json
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '.local' / 'discovery'
OUT.mkdir(parents=True, exist_ok=True)
env = {}
for line in (ROOT / '.env').read_text(encoding='utf-8-sig').splitlines():
    if '=' in line and not line.lstrip().startswith('#'):
        k, v = line.split('=', 1)
        env[k.strip()] = v.strip().strip('\"\'')

urls = {
    'camara_deputados': 'https://dadosabertos.camara.leg.br/api/v2/deputados?itens=1&ordem=ASC&ordenarPor=nome',
    'tce_sp': 'https://transparencia.tce.sp.gov.br/api/json/despesas/adamantina/2025/1',
    'siconfi': 'https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo?an_exercicio=2025&nr_periodo=1&co_tipo_demonstrativo=RREO&id_ente=3500105&no_anexo=RREO-Anexo%2001',
    'cgu_spec': 'https://api.portaldatransparencia.gov.br/v3/api-docs',
    'cgu_orgaos': 'https://api.portaldatransparencia.gov.br/api-de-dados/orgaos-siafi?pagina=1',
    'tce_pi': 'https://sistemas.tce.pi.gov.br/api/portaldacidadania/prefeituras',
    'tce_rn': 'https://apidadosabertos.tce.rn.gov.br/swagger/v1/swagger.json',
    'tce_pe': 'https://sistemas.tce.pe.gov.br/DadosAbertos/UnidadesJurisdicionadas!json',
    'tce_ce': 'https://api-dados-abertos.tce.ce.gov.br/municipios',
    'tce_rs': 'https://dados.tce.rs.gov.br/api/3/action/package_search?q=educacao&rows=1',
    'compras': 'https://contratos.comprasnet.gov.br/api/contrato/ug/170001',
}
for name, url in urls.items():
    headers = {'Accept': 'application/json', 'User-Agent': 'farol/0.1'}
    if name.startswith('cgu'):
        headers['chave-api-dados'] = env.get('TRANSPARENCIA_API_KEY', '')
    try:
        response = requests.get(url, headers=headers, timeout=25)
        try:
            value = response.json()
        except ValueError:
            value = None
        if value is not None:
            (OUT / (name + '.json')).write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')
        shape = list(value)[:12] if isinstance(value, dict) else ('list: ' + str(len(value))) if isinstance(value, list) else 'non-JSON'
        print(name, response.status_code, shape, flush=True)
        if name == 'camara_deputados' and response.ok and value:
            deputy = value['dados'][0]['id']
            r = requests.get('https://dadosabertos.camara.leg.br/api/v2/deputados/{}/despesas'.format(deputy), params={'ano':2025,'mes':1,'itens':100}, timeout=25)
            (OUT / 'camara_despesas.json').write_text(r.text, encoding='utf-8')
            print('camara pilot deputy', deputy, 'HTTP', r.status_code, flush=True)
    except requests.RequestException as exc:
        print(name, type(exc).__name__, flush=True)
