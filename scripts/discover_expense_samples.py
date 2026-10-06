"""Resolve small pilot partitions against public endpoints."""
import json
from pathlib import Path
import requests

p = Path('.local/discovery')
env = dict(line.split('=', 1) for line in Path('.env').read_text(encoding='utf-8-sig').splitlines() if '=' in line and not line.lstrip().startswith('#'))
queries = {
 'camara_pilot': ('https://dadosabertos.camara.leg.br/api/v2/deputados/204554/despesas', {'ano':2025,'mes':1,'itens':100}),
 'cgu_pilot': ('https://api.portaldatransparencia.gov.br/api-de-dados/despesas/por-orgao', {'ano':2025,'orgaoSuperior':'26000','pagina':1}),
 'siconfi_pilot': ('https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo', {'an_exercicio':2025,'nr_periodo':1,'co_tipo_demonstrativo':'RREO','id_ente':3550308}),
 'tce_pi_pilot': ('https://sistemas.tce.pi.gov.br/api/portaldacidadania/despesas/1473', {'exercicio':2025}),
 'tce_pe_pilot': ('https://sistemas.tce.pe.gov.br/DadosAbertos/DespesasMunicipais!json', {'ano':2025,'mes':1,'codigoMunicipio':'P001'}),
 'tce_rs_pilot': ('https://dados.tce.rs.gov.br/dados/municipal/educacao-indice/2025.json', {}),
 'tce_rn_pilot': ('https://apidadosabertos.tce.rn.gov.br/api/BalancoOrcamentarioApi/Despesa/Json/2025/1/1', {}),
}
for name,(url,params) in queries.items():
 try:
  headers={'Accept':'application/json'}
  if name.startswith('cgu'): headers['chave-api-dados']=env.get('TRANSPARENCIA_API_KEY','').strip().strip('\"\'')
  r=requests.get(url,params=params,headers=headers,timeout=30)
  try: v=r.json()
  except ValueError: v=None
  if v is not None: (p/(name+'.json')).write_text(json.dumps(v,ensure_ascii=False),encoding='utf-8')
  values=v.get('dados',v.get('items',v.get('resposta',v))) if isinstance(v,dict) else v
  print(name,r.status_code,'rows',len(values) if isinstance(values,list) else 'not list','keys',list(values[0]) if isinstance(values,list) and values and isinstance(values[0],dict) else '',flush=True)
 except requests.RequestException as e: print(name,type(e).__name__,flush=True)
