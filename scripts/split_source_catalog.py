"""Regenerate domain catalogs without changing the curated despesas scope."""

from collections import defaultdict
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def main():
    docs = ROOT / "docs"
    catalog = yaml.safe_load((docs / "sources.yaml").read_text(encoding="utf-8"))
    grouped = defaultdict(list)
    for source in catalog["sources"]:
        grouped[source["domain"]].append(source)

    index = [
        "# Source categories",
        "",
        "Generated from [sources.yaml](sources.yaml), grouped by its existing `domain` field.",
        "Each source belongs to exactly one category; all original source metadata is retained.",
        "The totals describe the catalog, not live endpoint availability or lakehouse ingestion.",
        "",
        "[despesas.yaml](despesas.yaml) remains a separately curated, cross-category expense scope.",
        "It overlaps these categories and must not be added to their totals.",
        "Unlike that curated scope, the original catalog does not enumerate tool definitions;",
        "these files preserve declared tool counts and returned models without inventing tool mappings.",
        "",
        "| Category | Sources | Declared tools |",
        "|---|---:|---:|",
    ]
    seen = []
    for domain, sources in sorted(grouped.items()):
        required = sorted({s["auth"]["env_var"] for s in sources
                           if s.get("auth", {}).get("required") is True
                           and s["auth"].get("env_var")})
        conditional = sorted({s["auth"]["env_var"] for s in sources
                              if s.get("auth", {}).get("required") == "partial"
                              and s["auth"].get("env_var")})
        count = sum(s["tools_count"] for s in sources)
        category = {
            "catalog": f"mcp-brasil — {domain}",
            "version": "v1",
            "derived_from": "sources.yaml",
            "generated_from_commit": catalog["generated_from_commit"],
            "scope": {
                "definition": f"Fontes classificadas no domínio {domain} no catálogo original.",
                "includes": [s["id"] for s in sources],
                "excludes": "Fontes classificadas em outros domínios.",
                "classification": "source.domain; uma categoria por fonte",
            },
            "totals": {
                "sources": len(sources), "tools": count,
                "keys_required": required, "keys_conditional": conditional,
                "note": "Contagens declaradas no catálogo; não indicam endpoints testados ou dados carregados.",
            },
            "global_settings": catalog["global_settings"],
            "known_gaps": [
                "O catálogo original não enumera ferramentas, parâmetros ou question_router por fonte.",
                "Resultados de testes herdados não comprovam disponibilidade atual dos endpoints.",
            ],
            "sources": sources,
        }
        target = docs / f"{domain}.yaml"
        target.write_text(yaml.safe_dump(category, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")
        loaded = yaml.safe_load(target.read_text(encoding="utf-8"))
        assert loaded["sources"] == sources, f"Metadata changed: {domain}"
        seen.extend(s["id"] for s in loaded["sources"])
        index.append(f"| [{domain}]({domain}.yaml) | {len(sources)} | {count} |")

    assert len(seen) == len(set(seen)) == len(catalog["sources"])
    assert set(seen) == {s["id"] for s in catalog["sources"]}
    total_tools = sum(s["tools_count"] for s in catalog["sources"])
    assert total_tools == catalog["totals"]["tools"]
    index.extend([
        f"| **Total** | **{len(seen)}** | **{total_tools}** |", "",
        "Regenerate after editing the master catalog:", "",
        "```powershell", "python scripts/split_source_catalog.py", "```", "",
        "Requires PyYAML. Generated category files should be updated through the master catalog.", "",
    ])
    (docs / "source-categories.md").write_text("\n".join(index), encoding="utf-8")
    print(f"Verified {len(grouped)} categories, {len(seen)} unique sources, {total_tools} declared tools; source metadata unchanged.")


if __name__ == "__main__":
    main()
