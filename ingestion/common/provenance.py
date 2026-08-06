"""Provenance injection shared by every dlt source — MUST-goal per DEFINE."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterator

SOURCE_VERSION = "1.0.0"  # bump when a source's extraction logic changes


@dataclass(frozen=True)
class ProvenanceContext:
    source_url: str
    source_version: str = SOURCE_VERSION


def with_provenance(
    records: Iterator[dict[str, Any]], ctx: ProvenanceContext
) -> Iterator[dict[str, Any]]:
    """Stamp every record with source_url/extracted_at/source_version before it leaves ingestion."""
    extracted_at = datetime.now(timezone.utc).isoformat()
    for record in records:
        yield {
            **record,
            "_source_url": ctx.source_url,
            "_extracted_at": extracted_at,
            "_source_version": ctx.source_version,
        }
