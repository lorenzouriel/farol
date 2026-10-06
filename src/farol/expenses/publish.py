"""Build immutable gold releases; failed builds never replace the previous release."""
import json
import os
import subprocess
import uuid

from .ops import Operations


def build_release():
    ops = Operations()
    release = 'gold_r' + uuid.uuid4().hex[:16]
    try:
        ops.lock()
        ops.execute("INSERT INTO publication(release_id,status) VALUES(%s,'building')",(release,))
        env = dict(os.environ, FAROL_RELEASE_SCHEMA=release)
        result = subprocess.run([os.getenv('DBT_BIN','dbt'), 'build', '--project-dir', '/opt/lakehouse/dbt',
                                 '--profiles-dir','/opt/lakehouse/dbt'],env=env,check=False)
        if result.returncode:
            ops.execute("UPDATE publication SET status='failed',detail='dbt build or tests failed' WHERE release_id=%s",(release,))
            raise RuntimeError('Gold release failed; previous successful release is unchanged')
        ops.execute("UPDATE publication SET status='ready',detail='dbt models and tests passed; awaiting dashboard publication' WHERE release_id=%s",(release,))
        print(json.dumps({'release_schema':release,'status':'ready'}),flush=True)
        return release
    finally:
        ops.close()


if __name__ == '__main__':
    build_release()
