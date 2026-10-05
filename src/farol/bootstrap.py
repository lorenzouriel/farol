"""Create namespaces and verify Spark writes can be read by Trino."""
import os
import uuid

from pyspark.sql import SparkSession
from trino.dbapi import connect


def bootstrap():
    spark = SparkSession.builder.remote(os.getenv("SPARK_REMOTE", "sc://127.0.0.1:25002")).getOrCreate()
    connection = connect(host=os.getenv("TRINO_HOST", "127.0.0.1"),
                         port=int(os.getenv("TRINO_PORT", "18080")), user="farol", catalog="lake")
    cursor = connection.cursor()
    table = "lake.bronze.smoke_" + uuid.uuid4().hex
    created = False
    try:
        for schema in ("bronze", "silver", "gold"):
            spark.sql(f"CREATE NAMESPACE IF NOT EXISTS lake.{schema}").collect()
        spark.createDataFrame([(1, "farol")], "id int, project string").writeTo(table).using("iceberg").create()
        created = True
        cursor.execute(f"SELECT id, project FROM {table}")
        rows = cursor.fetchall()
        if rows != [[1, "farol"]]:
            raise RuntimeError(f"Unexpected cross-engine smoke result: {rows!r}")
        print("PASS: Spark -> Iceberg/Nessie/S3 -> Trino; bronze/silver/gold ready")
    finally:
        try:
            if created:
                spark.sql(f"DROP TABLE {table}").collect()
        finally:
            cursor.close()
            connection.close()
            spark.stop()


if __name__ == "__main__":
    bootstrap()
