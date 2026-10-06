"""Small CGU / contract discovery samples; credentials are never printed."""
import json
from pathlib import Path
import requests

env = dict(line.split('=',1) for line in Path('.env').read_text(encoding='utf-8-sig').splitlines() if '=' in line and not line.lstrip().startswith('#'))
headers={'Accept':'application/json','chave-api-dados':env.get('TRANSPARENCIA_API_KEY','').strip().strip('\"\'')}
queries={
 'funcional':('despesas/por-funcional-programatica',{'ano':2025,'funcao':'12','pagina':1}),
 'documentos':('despesas/documentos',{'unidadeGestora':'153001','dataEmissao':'02/01/2025','fase':1,'pagina':1}),
 'cartoes':('cartoes',{'codigoOrgao':'26298','mesExtratoInicio':'01/2025','mesExtratoFim':'01/2025','pagina':1}),
 'viagens':('viagens',{'codigoOrgao':'26298','dataIdaDe':'01/01/2025','dataIdaAte':'31/01/2025','dataRetornoDe':'01/01/2025','dataRetornoAte':'28/02/2025','pagina':1}),
 'emendas':('emendas',{'ano':2025,'pagina':1}),
 'covid':('coronavirus/movimento-liquido-despesa',{'mesAno':'202012','pagina':1}),
}
out=Path('.local/discovery')
for name,(path,params) in queries.items():
 try:
  r=requests.get('https://api.portaldatransparencia.gov.br/api-de-dados/'+path,params=params,headers=headers,timeout=25)
  v=r.json(); (out/('cgu_'+name+'.json')).write_text(json.dumps(v,ensure_ascii=False),encoding='utf-8')
  print(name,r.status_code,len(v) if isinstance(v,list) else 'object',list(v[0]) if isinstance(v,list) and v else list(v) if isinstance(v,dict) else '',flush=True)
 except (requests.RequestException,ValueError) as exc: print(name,type(exc).__name__,flush=True)
for ug in ['153001','170010']:
 try:
  r=requests.get('https://contratos.comprasnet.gov.br/api/contrato/ug/'+ug,timeout=25); v=r.json()
  (out/('compras_'+ug+'.json')).write_text(json.dumps(v,ensure_ascii=False),encoding='utf-8')
  print('compras',ug,r.status_code,len(v) if isinstance(v,list) else 'object',flush=True)
  if isinstance(v,list) and v:
   contract=v[0]['id']; print('contract',contract,list(v[0]),flush=True)
   for child in ['empenhos','faturas']:
    r=requests.get('https://contratos.comprasnet.gov.br/api/contrato/'+str(contract)+'/'+child,timeout=25); value=r.json()
    (out/('compras_'+child+'.json')).write_text(json.dumps(value,ensure_ascii=False),encoding='utf-8')
    print(child,r.status_code,len(value) if isinstance(value,list) else 'object',list(value[0]) if isinstance(value,list) and value else '',flush=True)
   break
 except (requests.RequestException,ValueError) as exc: print('compras',type(exc).__name__,flush=True)
