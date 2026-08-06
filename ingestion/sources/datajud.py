"""DataJud (CNJ) REST source — processos.

Elasticsearch-backed search API. Pagination is cursor-based via
`search_after`, using the last hit's `sort` value, and stops once a page
returns zero hits. `status_processual` and `instancia` are MUST-present on
every yielded record — never null — because a downstream dbt test rejects
null values there; both default to "desconhecido" when the source payload
does not resolve them.
"""
import os
from typing import Any, Iterator

import dlt
import requests

from ingestion.common.provenance import ProvenanceContext, with_provenance

BASE_URL = "https://api-publica.datajud.cnj.jus.br"
SEARCH_ENDPOINT = f"{BASE_URL}/api_publica_v2/_search"
PAGE_SIZE = 100
API_KEY_ENV = "DATAJUD_API_KEY"


@dlt.source
def datajud_source():
    return [processos()]


@dlt.resource(name="processos", write_disposition="append", primary_key="numero_processo")
def processos():
    ctx = ProvenanceContext(source_url=SEARCH_ENDPOINT)
    yield from with_provenance(_search_all(), ctx)


def _search_all() -> Iterator[dict[str, Any]]:
    api_key = os.environ.get(API_KEY_ENV, "")
    headers = {
        "Authorization": f"APIKey {api_key}",
        "Content-Type": "application/json",
    }
    search_after: list[Any] | None = None
    while True:
        body: dict[str, Any] = {"size": PAGE_SIZE, "query": {"match_all": {}}}
        if search_after is not None:
            body["search_after"] = search_after
            body["sort"] = [{"_id": "asc"}]
        else:
            body["sort"] = [{"_id": "asc"}]
        resp = requests.post(SEARCH_ENDPOINT, headers=headers, json=body, timeout=60)
        resp.raise_for_status()
        hits = resp.json().get("hits", {}).get("hits", [])
        if not hits:
            break
        for hit in hits:
            yield _flatten_hit(hit)
        search_after = hits[-1].get("sort")
        if search_after is None:
            break


def _flatten_hit(hit: dict[str, Any]) -> dict[str, Any]:
    source = hit.get("_source", {})
    flattened = dict(source)
    flattened["numero_processo"] = source.get("numeroProcesso", hit.get("_id"))
    flattened["classe_processual"] = source.get("classe", {}).get("nome")
    flattened["orgao_julgador"] = source.get("orgaoJulgador", {}).get("nome")
    flattened["status_processual"] = source.get("statusProcessual") or "desconhecido"
    flattened["instancia"] = source.get("instancia") or source.get("grau") or "desconhecido"
    return flattened
