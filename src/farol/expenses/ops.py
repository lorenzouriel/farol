"""Operational state separate from Airflow metadata, with explicit migrations."""
import json
import os

import psycopg2
from psycopg2.extras import RealDictCursor


class Operations:
    def __init__(self):
        args = dict(host=os.getenv('OPS_HOST', 'meta-db'), user='lakehouse',
                    password=os.environ['META_DB_PASSWORD'])
        admin = psycopg2.connect(dbname='postgres', **args)
        admin.autocommit = True
        with admin.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname='farol_ops'")
            if cur.fetchone() is None:
                cur.execute('CREATE DATABASE farol_ops')
        admin.close()
        self.db = psycopg2.connect(dbname='farol_ops', **args)
        self.db.autocommit = True
        self.execute('''CREATE TABLE IF NOT EXISTS ingestion_run (
            run_id text PRIMARY KEY, resource text NOT NULL, partition_key text NOT NULL,
            config_hash text NOT NULL, status text NOT NULL, started_at timestamptz NOT NULL DEFAULT now(),
            finished_at timestamptz, record_count bigint, projected_count bigint,
            error text, source text NOT NULL)''')
        self.execute('''CREATE TABLE IF NOT EXISTS request_page (
            run_id text NOT NULL REFERENCES ingestion_run, page integer NOT NULL,
            request_hash text NOT NULL, status integer NOT NULL, content_type text,
            object_key text NOT NULL, sha256 text NOT NULL, bytes bigint NOT NULL,
            PRIMARY KEY(run_id,page))''')
        self.execute('ALTER TABLE request_page ADD COLUMN IF NOT EXISTS request_url text')
        self.execute('ALTER TABLE request_page ADD COLUMN IF NOT EXISTS request_params jsonb')
        self.execute('ALTER TABLE request_page ADD COLUMN IF NOT EXISTS fetched_at timestamptz DEFAULT now()')
        self.execute('''CREATE TABLE IF NOT EXISTS checkpoint (
            resource text NOT NULL, partition_key text NOT NULL, run_id text NOT NULL REFERENCES ingestion_run,
            completed_at timestamptz NOT NULL DEFAULT now(), PRIMARY KEY(resource,partition_key))''')
        self.execute('''CREATE TABLE IF NOT EXISTS quality_result (
            run_id text PRIMARY KEY REFERENCES ingestion_run, passed boolean NOT NULL,
            detail text NOT NULL, checked_at timestamptz NOT NULL DEFAULT now())''')
        self.execute('''CREATE TABLE IF NOT EXISTS publication (
            release_id text PRIMARY KEY, status text NOT NULL, detail text,
            created_at timestamptz NOT NULL DEFAULT now())''')

    def execute(self, query, values=()):
        with self.db.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, values)
            return list(cur.fetchall()) if cur.description else []

    def lock(self):
        if not self.execute('SELECT pg_try_advisory_lock(726041) AS locked')[0]['locked']:
            raise RuntimeError('Another expense ingestion or publication is running')

    def close(self):
        self.db.close()  # Releases session advisory lock.
