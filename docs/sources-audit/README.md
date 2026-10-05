# Source endpoint audit

Start with [the source and endpoint tables](report.md). The audit covers all 72 catalog entries: 70 have upstream URLs, and `rename` / `redator` have none. All 492 distinct catalog URLs per source were attempted, plus 33 representative or parameterized queries, on 2026-10-04.

| Result | Requests |
|---|---:|
| Successful response (data, file sample, service metadata, or expected scraped page) | 212 |
| Authentication/access blocked (401/403) | 97 |
| Other HTTP error | 131 |
| Unexpected HTML; data unverified | 39 |
| Connection, TLS, or timeout failure | 46 |
| Total | 525 |

49 sources had at least one successful response. That does not certify every endpoint or client operation. Network errors do not establish global downtime. Some failures are incomplete URL prefixes or missing credentials; the parameterized follow-ups are recorded separately.

The test read 36,606,616 response-body bytes. Of 91 dataset URLs, 79 returned file samples and advertised sizes totaling 2,765,572,807 bytes (about 2.77 GB). This is a **partial server-reported download total**, excluding the 12 unverified files, API pagination, and archive expansion. Full database row counts and storage requirements remain unknown.

Notable dataset results:

- `anac_vra`: January–September 2024 URLs returned 404; October–December returned file samples.
- `anac_tarifas`: the download URL returned HTML rather than the expected dataset.
- `inep_censo_escolar` and `inep_enem`: download connections failed in this environment.

Files:

- [report.md](report.md): table for each source and each request, with observed fields, array counts, status, body bytes, server size, and elapsed time.
- [results.json](results.json): structured evidence, including exact requested/final URLs, timestamps, observed field types, body previews and sample hashes.
- [results.jsonl](results.jsonl): incremental request log.
- [declared-contracts.json](declared-contracts.json): catalog model fields, explicitly **not** live-verified upstream schemas.

JSON fields describe only the observed complete response. CSV fields are sampled headers. ZIP archive contents and full CSV record totals were not verified. Payload previews are excerpts, not complete response dumps. Tests use no API credentials and do not run a stress/load test.

To rerun, from the repository root with Python, `requests`, and `PyYAML` installed:

```powershell
python scripts/audit_sources.py
python scripts/audit_sources_followup.py
python scripts/audit_sources.py --render
```

The first command replaces the prior results. The second appends parameterized follow-ups, and the third rebuilds the report without network requests. Elapsed seconds include host queue time and must not be used as a server-performance benchmark.
