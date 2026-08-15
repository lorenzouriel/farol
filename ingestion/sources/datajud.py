"""DataJud (CNJ) REST source — processos.

Elasticsearch-backed search API scoped per-tribunal: there is no unified
search index across all courts (the previously-configured `api_publica_v2`
alias does not exist — confirmed 404 against the live API), so every
tribunal has its own alias (`api_publica_tjsp`, `api_publica_trf1`, ...).
TRIBUNAL_ALIASES below is the full list of all 91 public aliases, verified
one-by-one against the live API on 2026-08-15 (CNJ publishes no discovery
endpoint, so this list can drift as tribunals are added/renamed).

An unfiltered query on a single large tribunal (e.g. TJSP) returns 70M+
records with no date bound — nationwide that's several hundred million to
over a billion records, unrunnable in one pass. Every tribunal query is
therefore scoped to `filter_year` via `dataAjuizamento`, which the API
stores as a `yyyyMMddHHmmss` string (confirmed empirically — plain
`YYYY-MM-DD` range values silently match almost nothing).

Pagination is cursor-based via `search_after`, using the last hit's `sort`
value, and stops once a tribunal's page returns zero hits. A fixed delay
between requests plus retry-with-backoff on 429/5xx keep this under the
public API's (undocumented) rate limit across what is still a long-running,
tens-of-thousands-of-requests crawl. `status_processual` and `instancia`
are MUST-present on every yielded record — never null — because a
downstream dbt test rejects null values there; both default to
"desconhecido" when the source payload does not resolve them.
"""
import os
import sys
import time
from typing import Any, Iterator

import dlt
import requests

from ingestion.common.provenance import ProvenanceContext, with_provenance

BASE_URL = "https://api-publica.datajud.cnj.jus.br"
PAGE_SIZE = 100
API_KEY_ENV = "DATAJUD_API_KEY"
REQUEST_DELAY_SECONDS = 0.25
MAX_RETRIES = 5

TRIBUNAL_ALIASES = [
    "tst", "tse", "stj", "stm",
    "trf1", "trf2", "trf3", "trf4", "trf5", "trf6",
    "tjac", "tjal", "tjam", "tjap", "tjba", "tjce", "tjdft", "tjes", "tjgo",
    "tjma", "tjmg", "tjms", "tjmt", "tjpa", "tjpb", "tjpe", "tjpi", "tjpr",
    "tjrj", "tjrn", "tjro", "tjrr", "tjrs", "tjsc", "tjse", "tjsp", "tjto",
    "trt1", "trt2", "trt3", "trt4", "trt5", "trt6", "trt7", "trt8", "trt9",
    "trt10", "trt11", "trt12", "trt13", "trt14", "trt15", "trt16", "trt17",
    "trt18", "trt19", "trt20", "trt21", "trt22", "trt23", "trt24",
    "tre-ac", "tre-al", "tre-am", "tre-ap", "tre-ba", "tre-ce", "tre-df",
    "tre-es", "tre-go", "tre-ma", "tre-mg", "tre-ms", "tre-mt", "tre-pa",
    "tre-pb", "tre-pe", "tre-pi", "tre-pr", "tre-rj", "tre-rn", "tre-ro",
    "tre-rr", "tre-rs", "tre-sc", "tre-se", "tre-sp", "tre-to",
    "tjmmg", "tjmrs", "tjmsp",
]


@dlt.source
def datajud_source():
    return [processos()]


@dlt.resource(name="processos", write_disposition="append", primary_key="numero_processo")
def processos(filter_year: int = dlt.config.value):
    api_key = os.environ.get(API_KEY_ENV, "")
    headers = {
        "Authorization": f"APIKey {api_key}",
        "Content-Type": "application/json",
    }
    date_range = {
        "gte": f"{filter_year}0101000000",
        "lt": f"{filter_year + 1}0101000000",
    }
    total = len(TRIBUNAL_ALIASES)
    for i, alias in enumerate(TRIBUNAL_ALIASES, start=1):
        endpoint = f"{BASE_URL}/api_publica_{alias}/_search"
        ctx = ProvenanceContext(source_url=endpoint)
        started = time.monotonic()
        count = 0
        for record in with_provenance(_search_tribunal(endpoint, headers, date_range), ctx):
            count += 1
            yield record
        elapsed = time.monotonic() - started
        print(
            f"[datajud {i}/{total}] {alias}: {count} records in {elapsed:.0f}s",
            file=sys.stderr,
            flush=True,
        )


def _search_tribunal(
    endpoint: str, headers: dict[str, str], date_range: dict[str, str]
) -> Iterator[dict[str, Any]]:
    search_after: list[Any] | None = None
    while True:
        body: dict[str, Any] = {
            "size": PAGE_SIZE,
            "query": {"range": {"dataAjuizamento": date_range}},
            # sorting by the ES meta field `_id` is disallowed by this
            # cluster's fielddata settings, and the plain `id` source field
            # is `text`-mapped (unsortable) -- `id.keyword` is its sortable
            # sub-field and is guaranteed unique, making it a safe cursor.
            "sort": [{"id.keyword": "asc"}],
        }
        if search_after is not None:
            body["search_after"] = search_after
        resp = _post_with_retry(endpoint, headers, body)
        hits = resp.json().get("hits", {}).get("hits", [])
        if not hits:
            break
        for hit in hits:
            yield _flatten_hit(hit)
        search_after = hits[-1].get("sort")
        if search_after is None:
            break
        time.sleep(REQUEST_DELAY_SECONDS)


def _post_with_retry(
    endpoint: str, headers: dict[str, str], body: dict[str, Any]
) -> requests.Response:
    backoff = 1.0
    for attempt in range(MAX_RETRIES):
        resp = requests.post(endpoint, headers=headers, json=body, timeout=60)
        if resp.status_code == 429 or resp.status_code >= 500:
            if attempt == MAX_RETRIES - 1:
                resp.raise_for_status()
            wait = float(resp.headers.get("Retry-After", backoff))
            time.sleep(wait)
            backoff *= 2
            continue
        resp.raise_for_status()
        return resp
    raise RuntimeError("unreachable")  # pragma: no cover


def _flatten_hit(hit: dict[str, Any]) -> dict[str, Any]:
    source = hit.get("_source", {})
    flattened = dict(source)
    flattened["numero_processo"] = source.get("numeroProcesso", hit.get("_id"))
    flattened["classe_processual"] = source.get("classe", {}).get("nome")
    flattened["orgao_julgador"] = source.get("orgaoJulgador", {}).get("nome")
    flattened["status_processual"] = source.get("statusProcessual") or "desconhecido"
    flattened["instancia"] = source.get("instancia") or source.get("grau") or "desconhecido"
    return flattened
