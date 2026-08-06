"""Senado Federal REST/XML source — parlamentares.

`/senador/lista/atual` returns senators as XML by default; JSON is requested
explicitly via the Accept header. The response shape is nested and not
contractually stable, so the list is extracted defensively.
"""
import dlt
import requests

from ingestion.common.provenance import ProvenanceContext, with_provenance

BASE_URL = "https://legis.senado.leg.br/dadosabertos"


@dlt.source
def senado_source():
    return [parlamentares()]


@dlt.resource(
    name="parlamentares",
    write_disposition="merge",
    primary_key="IdentificacaoParlamentar__CodigoParlamentar",
)
def parlamentares():
    url = f"{BASE_URL}/senador/lista/atual"
    ctx = ProvenanceContext(source_url=url)
    resp = requests.get(url, headers={"Accept": "application/json"}, timeout=30)
    resp.raise_for_status()
    payload = resp.json()
    lista_parlamentar = payload.get("ListaParlamentarEmExercicio", {})
    parlamentares_bloco = lista_parlamentar.get("Parlamentares", {})
    registros = parlamentares_bloco.get("Parlamentar", [])
    if isinstance(registros, dict):
        registros = [registros]
    yield from with_provenance(iter(registros), ctx)
