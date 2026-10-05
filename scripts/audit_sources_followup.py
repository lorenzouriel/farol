"""Parameterized follow-ups for catalog URL prefixes; append evidence then render."""
import concurrent.futures as futures
import json
from audit_sources import OUT, probe

QUERIES = {
 'brasilapi': [
  'https://brasilapi.com.br/api/cep/v1/01001000',
  'https://brasilapi.com.br/api/ddd/v1/11',
  'https://brasilapi.com.br/api/feriados/v1/2026',
  'https://brasilapi.com.br/api/fipe/marcas/v1/carros',
 ],
 'b3': ['https://brapi.dev/api/quote/PETR4'],
 'anuncios_eleitorais': ['https://graph.facebook.com/v25.0/ads_archive?ad_reached_countries=%5B%22BR%22%5D&search_terms=educacao&ad_type=POLITICAL_AND_ISSUE_ADS&limit=1'],
 'ibge': ['https://servicodados.ibge.gov.br/api/v2/cnae/classes', 'https://servicodados.ibge.gov.br/api/v2/censos/nomes/maria'],
 'ipeadata': ['http://ipeadata.gov.br/api/odata4/Metadados?$top=1'],
 'bcb_olinda': ['https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/Moedas?$format=json'],
 'bacen': ['https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/ExpectativasMercadoAnuais?$top=1&$format=json'],
 'compras': ['https://pncp.gov.br/api/consulta/v1/' + p + '?dataInicial=20260901&dataFinal=20260901&pagina=1&tamanhoPagina=10&codigoModalidadeContratacao=6' for p in ['contratacoes/publicacao','contratacoes/atualizacao','contratos','contratos/atualizacao','atas','atas/atualizacao']],
 'spu_geo': ['https://geoportal-spunet.gestao.gov.br/geoserver/ows?service=WMS&request=GetCapabilities'],
 'tce_sp': ['https://transparencia.tce.sp.gov.br/api/json/despesas/adamantina/2024/1','https://transparencia.tce.sp.gov.br/api/json/receitas/adamantina/2024/1'],
}

if __name__ == '__main__':
    items = [dict(source=s,label='parameterized follow-up',catalog_url=None,url=u,protocol='rest',dataset=False) for s, urls in QUERIES.items() for u in urls]
    with (OUT / 'results.jsonl').open('a',encoding='utf-8') as log, futures.ThreadPoolExecutor(max_workers=8) as pool:
        for r in pool.map(probe,items):
            log.write(json.dumps(r,ensure_ascii=False)+'\n'); log.flush()
            print(r['source'],r['status'],r['outcome'],flush=True)
