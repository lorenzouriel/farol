"""Entry point: runs every source, lands raw Parquet in MinIO."""
import dlt

from ingestion.sources.camara import camara_source
from ingestion.sources.ceap import ceap_source
from ingestion.sources.datajud import datajud_source
from ingestion.sources.senado import senado_source
from ingestion.sources.tse_bulk import tse_bulk_source

SOURCES = {
    "camara": camara_source,
    "senado": senado_source,
    "tse_bulk": tse_bulk_source,
    "ceap": ceap_source,
    "datajud": datajud_source,
}


def run_single_source(source_name: str) -> None:
    pipeline = dlt.pipeline(
        pipeline_name=f"farol_raw_{source_name}",
        destination=dlt.destinations.filesystem(bucket_url="s3://farol-raw"),
        dataset_name="raw",
        loader_file_format="parquet",
    )
    info = pipeline.run(SOURCES[source_name]())
    print(info)
