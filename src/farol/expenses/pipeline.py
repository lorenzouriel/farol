"""Durable raw pages -> quality gate -> snapshot bronze -> operational coverage."""
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import uuid
from datetime import datetime, timezone

import boto3
import yaml
from pyspark.sql import SparkSession

from .contracts import ContractError, digest, validate_batch
from .http import extract
from .ops import Operations

ROOT = Path(os.getenv('FAROL_ROOT', '/opt/lakehouse'))
SCHEMA = 'run_id string, resource string, partition_key string, source string, row_ordinal long, raw_object_key string, record_hash string, raw_json string, normalized_json string, extracted_at string'
BATCH_SCHEMA = 'run_id string, resource string, partition_key string, source string, extracted_at string, record_count long, projected_count long'


def write_snapshot(spark, name, values, schema):
    spark.createDataFrame(values, schema).writeTo('lake.bronze.' + name).using('iceberg').createOrReplace()


def sync_tracking(spark, ops, config):
    runs = ops.execute('SELECT *, started_at::text AS extracted_at FROM ingestion_run ORDER BY started_at')
    fields = ['run_id','resource','partition_key','source','status','extracted_at','record_count','projected_count','error']
    write_snapshot(spark, 'ingestion_runs', [tuple(r[k] for k in fields) for r in runs],
                   'run_id string, resource string, partition_key string, source string, status string, extracted_at string, record_count long, projected_count long, error string')
    definitions = yaml.safe_load((ROOT/'docs/despesas.yaml').read_text(encoding='utf-8'))
    registry = []
    for source in definitions['sources']:
        for tool in source['tools']:
            matched = [(name,c) for name,c in config['resources'].items() if c['source']==source['id'] and tool['name'] in c.get('capabilities',[])]
            states = []
            for name,c in matched:
                recent = [r for r in runs if r['resource']==name]
                states.append((name,recent[-1]['status'] if recent else 'not_run', recent[-1]['error'] if recent else c.get('blocked_reason')))
            if not matched:
                status, reason = 'contract_pending', 'Verified route, required IDs, grain and pagination contract not yet implemented.'
                if tool['name']=='anexos_populares':
                    status, reason = 'offline_support', 'Static annex selection; not an upstream financial dataset.'
            elif any(s[1]=='complete' for s in states):
                status, reason = 'pilot_loaded', 'Only the explicitly configured partitions are covered; not full source coverage.'
            else:
                status = states[0][1]
                reason = states[0][2] or 'Awaiting bounded extraction.'
            registry.append((source['id'],tool['name'],tool['role'],status,reason,','.join(n for n,c in matched)))
    write_snapshot(spark,'capability_registry',registry,'source string, capability string, role string, status string, reason string, resources string')


def ingest_resource(name, cfg, ops, s3, spark, resume=False):
    signature = digest(cfg)
    old = ops.execute("SELECT run_id FROM ingestion_run WHERE resource=%s AND partition_key=%s AND config_hash=%s AND status IN ('failed','running') ORDER BY started_at DESC LIMIT 1", (name,cfg['partition'],signature)) if resume else []
    run_id = old[0]['run_id'] if old else uuid.uuid4().hex
    ops.execute('''INSERT INTO ingestion_run(run_id,resource,partition_key,config_hash,status,source)
        VALUES(%s,%s,%s,%s,'running',%s) ON CONFLICT(run_id) DO UPDATE SET status='running',error=NULL''',
        (run_id,name,cfg['partition'],signature,cfg['source']))
    headers = {'Accept':'application/json', 'User-Agent':'farol-expenses/0.1'}
    keys = {}
    def load_page(page, request_hash):
        cached = ops.execute('SELECT * FROM request_page WHERE run_id=%s AND page=%s AND request_hash=%s AND status=200', (run_id,page,request_hash))
        if not cached:
            return None
        record = cached[0]
        stream = s3.get_object(Bucket='warehouse', Key=record['object_key'])['Body']
        try:
            body = gzip.decompress(stream.read())
        finally:
            stream.close()
        if hashlib.sha256(body).hexdigest() != record['sha256']:
            raise ContractError('Raw page checksum mismatch')
        keys[page] = record['object_key']
        return record['status'],record['content_type'],body
    def save_page(page, request_hash, status, content_type, body, url, params):
        key = f'raw/{cfg["source"]}/{name}/{run_id}/{request_hash}/{page}-{uuid.uuid4().hex}.json.gz'
        s3.put_object(Bucket='warehouse',Key=key,Body=gzip.compress(body,mtime=0),ContentType='application/gzip')
        ops.execute('''INSERT INTO request_page(run_id,page,request_hash,status,content_type,object_key,sha256,bytes,request_url,request_params)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT(run_id,page) DO UPDATE SET request_hash=EXCLUDED.request_hash,status=EXCLUDED.status,
            content_type=EXCLUDED.content_type,object_key=EXCLUDED.object_key,sha256=EXCLUDED.sha256,bytes=EXCLUDED.bytes,
            request_url=EXCLUDED.request_url,request_params=EXCLUDED.request_params,fetched_at=now()''',
            (run_id,page,request_hash,status,content_type,key,hashlib.sha256(body).hexdigest(),len(body),url,json.dumps(params)))
        keys[page] = key
    try:
        if not cfg.get('enabled', True):
            raise ContractError(cfg['blocked_reason'])
        if cfg.get('auth_env'):
            token = os.getenv(cfg['auth_env'], '')
            if not token or token == 'your_api_key_here':
                raise ContractError('Configured API credential missing or placeholder')
            headers[cfg['auth_header']] = token
        extracted = extract(cfg,headers,load_page,save_page)
        projected = validate_batch([r for page,i,r in extracted], cfg)
        timestamp = datetime.now(timezone.utc).isoformat()
        observations = [(run_id,name,cfg['partition'],cfg['source'],i,keys[page],digest(record),
                         json.dumps(record,ensure_ascii=False,default=str),json.dumps(projected[i],ensure_ascii=False) if projected[i] is not None else None,timestamp)
                        for i,(page,_,record) in enumerate(extracted)]
        # Resuming a run may follow a crash after the append; remove only this unpublished run.
        spark.sql(f"DELETE FROM lake.bronze.expense_observation WHERE run_id = '{run_id}'").collect()
        if observations:
            spark.createDataFrame(observations,SCHEMA).writeTo('lake.bronze.expense_observation').append()
        count = sum(v is not None for v in projected)
        spark.sql(f"DELETE FROM lake.bronze.complete_batch WHERE run_id = '{run_id}'").collect()
        spark.createDataFrame([(run_id,name,cfg['partition'],cfg['source'],timestamp,len(extracted),count)],BATCH_SCHEMA).writeTo('lake.bronze.complete_batch').append()
        ops.execute("UPDATE ingestion_run SET status='complete',finished_at=now(),record_count=%s,projected_count=%s WHERE run_id=%s",(len(extracted),count,run_id))
        ops.execute('''INSERT INTO checkpoint(resource,partition_key,run_id) VALUES(%s,%s,%s)
            ON CONFLICT(resource,partition_key) DO UPDATE SET run_id=EXCLUDED.run_id,completed_at=now()''',(name,cfg['partition'],run_id))
        ops.execute('INSERT INTO quality_result(run_id,passed,detail) VALUES(%s,true,%s) ON CONFLICT(run_id) DO UPDATE SET passed=true,detail=EXCLUDED.detail', (run_id,'Pagination, scope, financial types and declared grain passed'))
        print(f'{name}: complete ({len(extracted)} raw / {count} projected records)',flush=True)
        return True
    except Exception as exc:
        # Never persist request exception strings that could contain headers or sensitive URLs.
        detail = str(exc) if isinstance(exc,ContractError) else type(exc).__name__
        state = 'blocked' if not cfg.get('enabled',True) else 'quarantined' if isinstance(exc,ContractError) else 'failed'
        ops.execute('UPDATE ingestion_run SET status=%s,error=%s,finished_at=now() WHERE run_id=%s',(state,detail,run_id))
        ops.execute('INSERT INTO quality_result(run_id,passed,detail) VALUES(%s,false,%s) ON CONFLICT(run_id) DO UPDATE SET passed=false,detail=EXCLUDED.detail',(run_id,detail))
        print(f'{name}: {state} ({detail})',flush=True)
        return False


def run(selected=None, resume=False):
    config = yaml.safe_load((ROOT/'conf/despesas.yml').read_text(encoding='utf-8'))
    if selected and any(x not in config['resources'] for x in selected):
        raise ValueError('Unknown resource selection')
    ops = Operations()
    spark = None
    try:
        ops.lock()
        spark = SparkSession.builder.remote(os.environ['SPARK_REMOTE']).getOrCreate()
        for namespace in ('bronze','silver','gold'):
            spark.sql(f'CREATE NAMESPACE IF NOT EXISTS lake.{namespace}').collect()
        for table,schema in [('expense_observation',SCHEMA),('complete_batch',BATCH_SCHEMA)]:
            if not spark.catalog.tableExists('lake.bronze.'+table):
                spark.createDataFrame([],schema).writeTo('lake.bronze.'+table).using('iceberg').create()
        s3 = boto3.client('s3',endpoint_url=os.environ['S3_ENDPOINT'],
                          aws_access_key_id=os.environ['S3_ACCESS_KEY'],aws_secret_access_key=os.environ['S3_SECRET_KEY'],region_name='us-east-1')
        outcomes = []
        for name,resource in config['resources'].items():
            if selected and name not in selected:
                continue
            outcomes.append(ingest_resource(name,dict(config['defaults'],**resource),ops,s3,spark,resume))
        sync_tracking(spark,ops,config)
        return all(outcomes)
    finally:
        if spark:
            spark.stop()
        ops.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--resource',action='append')
    parser.add_argument('--resume',action='store_true')
    args = parser.parse_args()
    raise SystemExit(0 if run(args.resource,args.resume) else 2)
