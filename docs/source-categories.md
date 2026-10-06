# Source categories

Generated from [sources.yaml](sources.yaml), grouped by its existing `domain` field.
Each source belongs to exactly one category; all original source metadata is retained.
The totals describe the catalog, not live endpoint availability or lakehouse ingestion.

[despesas.yaml](despesas.yaml) remains a separately curated, cross-category expense scope.
It overlaps these categories and must not be added to their totals.
Unlike that curated scope, the original catalog does not enumerate tool definitions;
these files preserve declared tool counts and returned models without inventing tool mappings.

| Category | Sources | Declared tools |
|---|---:|---:|
| [agentes](agentes.yaml) | 1 | 5 |
| [aviacao](aviacao.yaml) | 5 | 29 |
| [compras_publicas](compras_publicas.yaml) | 2 | 34 |
| [dados_abertos_utilidades](dados_abertos_utilidades.yaml) | 4 | 45 |
| [economia](economia.yaml) | 4 | 26 |
| [educacao](educacao.yaml) | 4 | 21 |
| [eleitoral](eleitoral.yaml) | 7 | 48 |
| [energia_infraestrutura](energia_infraestrutura.yaml) | 3 | 15 |
| [geografia_estatistica](geografia_estatistica.yaml) | 1 | 9 |
| [judiciario](judiciario.yaml) | 2 | 18 |
| [legislativo_executivo](legislativo_executivo.yaml) | 3 | 41 |
| [meio_ambiente](meio_ambiente.yaml) | 3 | 11 |
| [mercado_financeiro_noticias](mercado_financeiro_noticias.yaml) | 3 | 16 |
| [saude](saude.yaml) | 8 | 63 |
| [seguranca_publica](seguranca_publica.yaml) | 4 | 23 |
| [transparencia_fiscalizacao](transparencia_fiscalizacao.yaml) | 18 | 137 |
| **Total** | **72** | **541** |

Regenerate after editing the master catalog:

```powershell
python scripts/split_source_catalog.py
```

Requires PyYAML. Generated category files should be updated through the master catalog.
