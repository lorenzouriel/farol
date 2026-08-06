"""Unit tests for ingestion/common/provenance.py.

with_provenance() is a pure generator: no network, no mocking needed.
Covers the MUST-goal from DEFINE that every record leaving ingestion
carries _source_url / _extracted_at / _source_version.
"""
from __future__ import annotations

from datetime import datetime

import pytest

from ingestion.common.provenance import ProvenanceContext, with_provenance

PROVENANCE_KEYS = {"_source_url", "_extracted_at", "_source_version"}


@pytest.fixture
def sample_records() -> list[dict]:
    return [
        {"id": 1, "nome": "Alice"},
        {"id": 2, "nome": "Bob"},
        {"id": 3, "nome": "Carol"},
    ]


@pytest.fixture
def ctx() -> ProvenanceContext:
    return ProvenanceContext(source_url="https://example.com/api")


class TestWithProvenance:
    """Tests for with_provenance()."""

    def test_every_record_gets_provenance_keys(self, sample_records, ctx):
        """Every yielded record carries the 3 provenance fields with correct values."""
        results = list(with_provenance(iter(sample_records), ctx))

        assert len(results) == len(sample_records)
        for record in results:
            assert record["_source_url"] == "https://example.com/api"
            assert record["_source_version"] == "1.0.0"
            # Must be a parseable ISO timestamp.
            parsed = datetime.fromisoformat(record["_extracted_at"])
            assert isinstance(parsed, datetime)

    def test_custom_source_version_is_respected(self, sample_records):
        """A non-default source_version on the context is propagated verbatim."""
        ctx = ProvenanceContext(source_url="https://example.com/api", source_version="2.3.1")

        results = list(with_provenance(iter(sample_records), ctx))

        assert all(r["_source_version"] == "2.3.1" for r in results)

    def test_original_keys_and_values_preserved(self, sample_records, ctx):
        """Original dict keys/values survive unchanged, alongside the 3 new keys."""
        results = list(with_provenance(iter(sample_records), ctx))

        for original, stamped in zip(sample_records, results):
            for key, value in original.items():
                assert stamped[key] == value
            # Exactly the original keys plus the 3 provenance keys, nothing else.
            assert set(stamped.keys()) == set(original.keys()) | PROVENANCE_KEYS

    def test_empty_iterator_yields_nothing(self, ctx):
        """An empty input iterator yields nothing and does not crash."""
        results = list(with_provenance(iter([]), ctx))

        assert results == []

    def test_all_records_share_same_extracted_at(self, sample_records, ctx):
        """A single with_provenance() call stamps a consistent extraction timestamp."""
        results = list(with_provenance(iter(sample_records), ctx))

        timestamps = {r["_extracted_at"] for r in results}
        assert len(timestamps) == 1
