"""Câmara CEAP (cota parlamentar) bulk source — despesas.

CEAP's bulk files follow their own layout, distinct from the rest of the
Câmara API — see docs/farolv1.md section 3. Deputies have 90 days to submit
reimbursement receipts, so a given year's totals are never assumed complete
here; completeness windows are handled downstream in dbt.
"""
import csv
import io
import os
import tempfile
import zipfile
from typing import Any, Iterator

import dlt
import requests

from ingestion.common.provenance import ProvenanceContext, with_provenance

BASE_URL = "https://www.camara.leg.br/cotas"


@dlt.source
def ceap_source():
    return [despesas()]


@dlt.resource(
    name="despesas",
    write_disposition="merge",
    primary_key=["ideDocumento", "numAno", "numMes"],
)
def despesas(years: list[int] = dlt.config.value):
    for ano in years:
        url = f"{BASE_URL}/Ano-{ano}.csv.zip"
        ctx = ProvenanceContext(source_url=url)
        yield from with_provenance(_rows_from_zip(url), ctx)


def _rows_from_zip(url: str) -> Iterator[dict[str, Any]]:
    # delete=False + explicit close before reopening: on Windows, a
    # NamedTemporaryFile holds an exclusive lock while open, so reopening it
    # via zipfile.ZipFile in the same process raises PermissionError.
    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp_file:
        tmp_path = tmp_file.name
        with requests.get(url, stream=True, timeout=120) as resp:
            resp.raise_for_status()
            for chunk in resp.iter_content(chunk_size=8192):
                tmp_file.write(chunk)
    try:
        with zipfile.ZipFile(tmp_path) as archive:
            for member_name in archive.namelist():
                if not member_name.lower().endswith(".csv"):
                    continue
                with archive.open(member_name) as member_file:
                    text_stream = io.TextIOWrapper(member_file, encoding="utf-8")
                    reader = csv.DictReader(text_stream, delimiter=";")
                    yield from reader
    finally:
        os.unlink(tmp_path)
