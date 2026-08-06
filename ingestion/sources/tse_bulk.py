"""TSE Dados Abertos bulk source — candidatos.

TSE publishes bulk data as ZIP files containing pipe-delimited CSVs per
election year, not a paginated API. Each ZIP is streamed to a temp file,
opened member by member, and parsed with `latin-1` encoding — the actual
encoding of TSE's bulk CSVs.
"""
import csv
import io
import tempfile
import zipfile
from typing import Any, Iterator

import dlt
import requests

from ingestion.common.provenance import ProvenanceContext, with_provenance

BASE_URL = "https://dadosabertos.tse.jus.br"


@dlt.source
def tse_bulk_source():
    return [candidatos()]


@dlt.resource(name="candidatos", write_disposition="merge", primary_key="SQ_CANDIDATO")
def candidatos(election_years: list[int] = dlt.config.value):
    for ano in election_years:
        url = f"{BASE_URL}/candidatos/consulta_cand_{ano}.zip"
        ctx = ProvenanceContext(source_url=url)
        yield from with_provenance(_rows_from_zip(url), ctx)


def _rows_from_zip(url: str) -> Iterator[dict[str, Any]]:
    with tempfile.NamedTemporaryFile(suffix=".zip") as tmp_file:
        with requests.get(url, stream=True, timeout=120) as resp:
            resp.raise_for_status()
            for chunk in resp.iter_content(chunk_size=8192):
                tmp_file.write(chunk)
        tmp_file.flush()
        with zipfile.ZipFile(tmp_file.name) as archive:
            for member_name in archive.namelist():
                if not member_name.lower().endswith(".csv"):
                    continue
                with archive.open(member_name) as member_file:
                    text_stream = io.TextIOWrapper(member_file, encoding="latin-1")
                    reader = csv.DictReader(text_stream, delimiter=";")
                    yield from reader
