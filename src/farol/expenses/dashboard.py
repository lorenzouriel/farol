"""Create a new versioned Superset dashboard only after gold quality gates pass."""
import json
import os
import re

import requests

from .ops import Operations

MARTS = {
    'mart_cobertura_fontes': 'Coverage — 42 capabilities (pilot scope)',
    'mart_ingestion_runs': 'Ingestion status and failures',
    'mart_execucao_orgao_periodo': 'Federal execution — separate committed / liquidated / paid',
    'mart_execucao_municipal': 'SP movements — cancellations shown separately',
    'mart_demonstrativos_fiscais': 'RREO / RGF / DCA expense cells — different measure bases',
    'mart_indicadores_rs': 'RS MDE — published percentages, not additive',
    'mart_execucao_pi_anual': 'PI annual totals — not expense transactions',
    'mart_ceap_deputado_mes': 'CEAP — empty if no validated pilot data',
    'mart_execucao_funcao_periodo': 'Education execution — selected action only',
    'mart_emendas': 'Amendment execution — selected amendment only',
    'mart_contrato_empenhos': 'Linked commitments — may overlap CGU',
    'mart_contrato_faturas': 'Contract invoices — not payment evidence',
}


def publish_dashboard(release=None):
    ops = Operations()
    try:
        ops.lock()
        choices = ops.execute("SELECT release_id FROM publication WHERE status='ready' ORDER BY created_at DESC LIMIT 1") if release is None else ops.execute("SELECT release_id FROM publication WHERE status='ready' AND release_id=%s",(release,))
        if not choices:
            raise RuntimeError('No validated release awaiting publication')
        release = choices[0]['release_id']
        if not re.fullmatch(r'gold_r[0-9a-f]{16}',release):
            raise ValueError('Invalid release schema')
        base = os.getenv('SUPERSET_URL','http://127.0.0.1:8088').rstrip('/')
        session = requests.Session()
        def call(method,path,**kwargs):
            response = session.request(method,base+'/api/v1/'+path,timeout=60,**kwargs)
            response.raise_for_status()
            return response.json()
        def inventory(kind):
            result = []
            for page in range(100):
                data = call('GET',kind+'/',params={'q':json.dumps({'page':page,'page_size':100})})
                result.extend(data['result'])
                if len(result) >= data['count']:
                    return result
            raise RuntimeError('Superset inventory page cap reached')
        token = call('POST','security/login',json={'username':'admin','password':os.environ['SUPERSET_ADMIN_PASSWORD'],'provider':'db','refresh':True})['access_token']
        session.headers['Authorization'] = 'Bearer '+token
        session.headers['X-CSRFToken'] = call('GET','security/csrf_token/')['result']
        databases = inventory('database')
        existing = [x['id'] for x in databases if x['database_name']=='Farol']
        database_id = existing[0] if existing else call('POST','database/',json={
            'database_name':'Farol','sqlalchemy_uri':'trino://farol@trino:8080/lake','expose_in_sqllab':True})['id']
        dashboards, datasets, charts = inventory('dashboard'), inventory('dataset'), inventory('chart')
        matching = [d['id'] for d in dashboards if d.get('slug')=='farol-'+release]
        dashboard_id = matching[0] if matching else call('POST','dashboard/',json={
            'dashboard_title':'Farol despesas v1 — bounded pilot '+release,
            'published':False,'slug':'farol-'+release})['id']
        layout = {'DASHBOARD_VERSION_KEY':'v2',
                  'ROOT_ID':{'id':'ROOT_ID','type':'ROOT','children':['GRID_ID']},
                  'GRID_ID':{'id':'GRID_ID','type':'GRID','children':[],'parents':['ROOT_ID']}}
        for index,(table,label) in enumerate(MARTS.items()):
            matching = [d['id'] for d in datasets if d.get('schema')==release and d.get('table_name')==table]
            dataset_id = matching[0] if matching else call('POST','dataset/',json={'database':database_id,'schema':release,'table_name':table})['id']
            dataset = call('GET',f'dataset/{dataset_id}')['result']
            columns = [c['column_name'] for c in dataset['columns']]
            params = {'viz_type':'table','query_mode':'raw','all_columns':columns,
                      'row_limit':1000,'datasource':f'{dataset_id}__table'}
            context = {'datasource':{'id':dataset_id,'type':'table'},'force':False,
                       'queries':[{'columns':columns,'metrics':[],'filters':[],'row_limit':1000}],
                       'form_data':params,'result_format':'json','result_type':'full'}
            # Execute the chart query before exposing the dashboard.
            checked = call('POST','chart/data',json=context)
            if any(item.get('error') for item in checked.get('result',[])):
                raise RuntimeError('Superset data query failed for '+table)
            body = {'slice_name':label+' / '+release,'viz_type':'table',
                'datasource_id':dataset_id,'datasource_type':'table','params':json.dumps(params),
                'query_context':json.dumps(context),'dashboards':[dashboard_id]}
            matching = [c['id'] for c in charts if c.get('slice_name')==body['slice_name']]
            if matching:
                chart_id = matching[0]
                call('PUT',f'chart/{chart_id}',json=body)
            else:
                chart_id = call('POST','chart/',json=body)['id']
            row,chart = f'ROW-{index}',f'CHART-{chart_id}'
            layout['GRID_ID']['children'].append(row)
            layout[row] = {'id':row,'type':'ROW','parents':['ROOT_ID','GRID_ID'],'children':[chart],'meta':{'background':'BACKGROUND_TRANSPARENT'}}
            layout[chart] = {'id':chart,'type':'CHART','parents':['ROOT_ID','GRID_ID',row],'children':[],
                             'meta':{'chartId':chart_id,'sliceName':label,'width':12,'height':65}}
        call('PUT',f'dashboard/{dashboard_id}',json={'published':True,'position_json':json.dumps(layout)})
        path = '/superset/dashboard/'+str(dashboard_id)+'/'
        ops.execute("UPDATE publication SET status='published',detail=%s WHERE release_id=%s",(json.dumps({'dashboard_path':path,'dashboard_id':dashboard_id}),release))
        print(json.dumps({'release':release,'dashboard_path':path,'charts':len(MARTS)}),flush=True)
        return path
    finally:
        ops.close()


if __name__ == '__main__':
    publish_dashboard()
