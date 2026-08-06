"""Tests for the Câmara pagination trap (DEFINE AT-002).

AT-002: Given the Câmara API returns `dados: []` for a page beyond the last
page, when the dlt resource paginates, then ingestion terminates cleanly
without treating the empty page as an error, and no partial/corrupt raw
records are written.

`requests.get` is mocked with `unittest.mock.patch` from the standard
library — there is no existing test suite/convention in this repo yet, and
stdlib `unittest.mock` avoids introducing a new test dependency (e.g.
pytest-mock) purely for this. `deputados()` is a `@dlt.resource`-decorated
generator function; iterating it directly (`list(deputados())`) outside of
a `pipeline.run()` call drives the underlying generator without going
through dlt's extract/normalize pipeline stages, which is the standard way
to unit test a dlt resource's own logic in isolation.
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
import requests

from ingestion.sources.camara import deputados

PROVENANCE_KEYS = {"_source_url", "_extracted_at", "_source_version"}


def _make_response(dados: list[dict]) -> MagicMock:
    """Build a mock `requests.Response`-like object for a given `dados` page."""
    response = MagicMock()
    response.json.return_value = {"dados": dados}
    response.raise_for_status.return_value = None
    return response


class TestDeputadosPaginationTermination:
    """AT-002: empty `dados: []` page ends the loop cleanly, not as an error."""

    @patch("ingestion.sources.camara.requests.get")
    def test_terminates_on_empty_dados_page(self, mock_get):
        """Page 1 has 2 records, page 2 is the empty-page pagination trap."""
        page_1 = _make_response([{"id": 1, "nome": "A"}, {"id": 2, "nome": "B"}])
        page_2 = _make_response([])
        mock_get.side_effect = [page_1, page_2]

        records = list(deputados())

        assert len(records) == 2
        assert mock_get.call_count == 2

    @patch("ingestion.sources.camara.requests.get")
    def test_yielded_records_carry_provenance(self, mock_get):
        """Every record surviving the pagination loop is provenance-stamped."""
        page_1 = _make_response([{"id": 1, "nome": "A"}, {"id": 2, "nome": "B"}])
        page_2 = _make_response([])
        mock_get.side_effect = [page_1, page_2]

        records = list(deputados())

        assert [r["id"] for r in records] == [1, 2]
        for record in records:
            assert PROVENANCE_KEYS.issubset(record.keys())
            assert record["_source_url"].startswith(
                "https://dadosabertos.camara.leg.br/api/v2/deputados"
            )
            assert record["_source_version"] == "1.0.0"

    @patch("ingestion.sources.camara.requests.get")
    def test_no_partial_or_corrupt_records_after_empty_page(self, mock_get):
        """Only the real 2 records from page 1 survive — nothing from the empty page."""
        page_1 = _make_response([{"id": 1, "nome": "A"}, {"id": 2, "nome": "B"}])
        page_2 = _make_response([])
        mock_get.side_effect = [page_1, page_2]

        records = list(deputados())

        assert all(record.get("id") is not None for record in records)
        assert len(records) == 2


class TestDeputadosGenuineErrorsPropagate:
    """Real HTTP failures (e.g. a 500) must fail loudly, not be swallowed."""

    @patch("ingestion.sources.camara.requests.get")
    def test_http_error_on_first_page_propagates(self, mock_get):
        """A real requests.HTTPError on page 1 is not treated as benign like dados: []."""
        mock_get.side_effect = requests.HTTPError("500 Server Error")

        with pytest.raises(requests.HTTPError):
            list(deputados())

    @patch("ingestion.sources.camara.requests.get")
    def test_http_error_via_raise_for_status_propagates(self, mock_get):
        """A response object that raises on .raise_for_status() also propagates."""
        error_response = MagicMock()
        error_response.raise_for_status.side_effect = requests.HTTPError(
            "500 Server Error"
        )
        mock_get.return_value = error_response

        with pytest.raises(requests.HTTPError):
            list(deputados())
