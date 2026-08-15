"""Câmara dos Deputados REST source — deputados + proposições.

Handles the known pagination trap: /api/v2 returns `dados: []` (not a 404)
once you page past the last result — see docs/farolv1.md section 2.

The /deputados list endpoint does not return `cpf` or `nomeEleitoral` at
all (confirmed against the live API) -- both only exist on the per-deputy
detail endpoint (/deputados/{id}). CPF-keyed identity resolution
(dim_politico) needs cpf on every Câmara record, so each listed deputy is
enriched with one extra detail-endpoint call.
"""
from typing import Any, Iterator

import dlt
import requests

from ingestion.common.provenance import ProvenanceContext, with_provenance

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"
PAGE_SIZE = 100  # API max


@dlt.source
def camara_source():
    return [deputados(), proposicoes()]


@dlt.resource(name="deputados", write_disposition="merge", primary_key="id")
def deputados():
    url = f"{BASE_URL}/deputados"
    ctx = ProvenanceContext(source_url=url)
    page = 1
    while True:
        resp = requests.get(url, params={"pagina": page, "itens": PAGE_SIZE}, timeout=30)
        resp.raise_for_status()
        dados = resp.json()["dados"]
        if not dados:
            break
        yield from with_provenance(_enrich_with_detail(dados), ctx)
        page += 1


def _enrich_with_detail(dados: list[dict[str, Any]]) -> Iterator[dict[str, Any]]:
    for dep in dados:
        detail_url = f"{BASE_URL}/deputados/{dep['id']}"
        resp = requests.get(detail_url, timeout=30)
        resp.raise_for_status()
        detail = resp.json().get("dados", {})
        ultimo_status = detail.get("ultimoStatus") or {}
        yield {
            **dep,
            "cpf": detail.get("cpf"),
            "nomeEleitoral": ultimo_status.get("nomeEleitoral"),
        }


@dlt.resource(name="proposicoes", write_disposition="append", primary_key="id")
def proposicoes(ano: int = dlt.config.value):
    url = f"{BASE_URL}/proposicoes"
    ctx = ProvenanceContext(source_url=url)
    page = 1
    while True:
        resp = requests.get(
            url, params={"ano": ano, "pagina": page, "itens": PAGE_SIZE}, timeout=30
        )
        resp.raise_for_status()
        dados = resp.json()["dados"]
        if not dados:
            break
        yield from with_provenance(iter(dados), ctx)
        page += 1
