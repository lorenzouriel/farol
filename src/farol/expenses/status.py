"""Print secret-free operational and release status."""
import json
import argparse
import os
import re
from .ops import Operations


def status(include_lake=False):
    ops=Operations()
    try:
        result = {
            'resources':ops.execute('''SELECT DISTINCT ON(resource) resource,source,status,
                record_count,projected_count,error,started_at FROM ingestion_run ORDER BY resource,started_at DESC'''),
            'raw_load':ops.execute('SELECT count(*) AS saved_pages,sum(bytes) AS response_body_bytes FROM request_page'),
            'releases':ops.execute('SELECT * FROM publication ORDER BY created_at DESC'),
        }
        if include_lake:
            from trino.dbapi import connect
            db=connect(host=os.environ['TRINO_HOST'],port=int(os.environ['TRINO_PORT']),user='farol',catalog='lake')
            cur=db.cursor()
            try:
                cur.execute('SELECT source,capability,role,status,reason,resources FROM lake.bronze.capability_registry ORDER BY source,capability')
                names=[c[0] for c in cur.description]
                result['capabilities']=[dict(zip(names,row)) for row in cur.fetchall()]
                cur.execute('SHOW TABLES FROM lake.silver')
                tables=[row[0] for row in cur.fetchall()]
                result['silver_record_counts']={}
                for name in tables:
                    if not re.fullmatch(r'[a-z_]+',name):
                        continue
                    cur.execute('SELECT count(*) FROM lake.silver.'+name)
                    result['silver_record_counts'][name]=cur.fetchone()[0]
                result['provenance_pages']=ops.execute('SELECT count(*) AS pages_with_exact_request FROM request_page WHERE request_url IS NOT NULL')[0]['pages_with_exact_request']
            finally:
                cur.close()
                db.close()
        return result
    finally:
        ops.close()


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--lake',action='store_true')
    args=parser.parse_args()
    print(json.dumps(status(args.lake),default=str,ensure_ascii=False,indent=2))
