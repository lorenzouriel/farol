# Despesas v1 capability checklist

Implementation snapshot after the verified pilot run (2026-10-05/06). This is not a live runtime health report.
`Pilot loaded` means only the configured partitions were verified. The lakehouse coverage mart refreshes this inventory on ingestion.

Coverage: **15 pilot loaded, 21 pending implementation, 4 blocked/deferred, 1 quarantined, and 1 offline support**. See [the exported runtime snapshot](despesas-v1-status.json).

| Source | Capability | Role | Implementation / evidence |
|---|---|---|---|
| transparencia | consultar_despesas_orgao | core | Pilot loaded: cgu_execucao_orgao |
| transparencia | consultar_despesas_funcional | core | Pilot loaded: cgu_funcional |
| transparencia | buscar_documentos_despesa | core | Pending implementation: verified query contract, identifiers and financial mapping. |
| transparencia | buscar_itens_empenho | core | Pending implementation: verified query contract, identifiers and financial mapping. |
| transparencia | consultar_despesas | core | Pending implementation: verified query contract, identifiers and financial mapping. |
| transparencia | buscar_empenhos_licitacao | core | Pending implementation: verified query contract, identifiers and financial mapping. |
| transparencia | buscar_cartoes_pagamento | core | Pending implementation: verified query contract, identifiers and financial mapping. |
| transparencia | consultar_viagens | core | Pending implementation: verified query contract, identifiers and financial mapping. |
| transparencia | buscar_viagens_orgao | core | Pending implementation: verified query contract, identifiers and financial mapping. |
| transparencia | detalhar_viagem | core | Pending implementation: verified query contract, identifiers and financial mapping. |
| transparencia | consultar_coronavirus_despesas | core | Pending implementation: verified query contract, identifiers and financial mapping. |
| transparencia | buscar_emendas | core | Pilot loaded: cgu_emendas |
| transparencia | buscar_documentos_emenda | core | Pending implementation: verified query contract, identifiers and financial mapping. |
| transparencia | listar_orgaos | lookup | Full lookup pagination deferred; pilot organization was validated by expense response. |
| camara | despesas_deputado | core | Implemented contract; sampled CEAP responses were empty and quarantined. |
| camara | listar_deputados | lookup | Pilot loaded: camara_deputados |
| camara | buscar_deputado | lookup | Pending implementation: verified query contract, identifiers and financial mapping. |
| siconfi | consultar_rreo | core | Pilot loaded: siconfi_rreo |
| siconfi | consultar_rgf | core | Pilot loaded: siconfi_rgf |
| siconfi | consultar_dca | core | Pilot loaded: siconfi_dca |
| siconfi | extrato_entregas | support | Pending implementation: verified query contract, identifiers and financial mapping. |
| siconfi | listar_anexos_relatorios | support | Pending implementation: verified query contract, identifiers and financial mapping. |
| siconfi | anexos_populares | support | Offline support; no upstream financial table. |
| siconfi | listar_entes | lookup | Pending implementation: verified query contract, identifiers and financial mapping. |
| compras | contratosgovbr_consultar_empenhos_contrato | core | Pilot loaded: compras_empenhos |
| compras | contratosgovbr_consultar_faturas_contrato | core | Pilot loaded: compras_faturas |
| compras | contratosgovbr_listar_contratos_unidade | lookup | Pilot loaded: compras_execucao |
| tce_sp | consultar_despesas_sp | core | Pilot loaded: tce_sp_despesas |
| tce_sp | listar_municipios_sp | lookup | Pilot loaded: tce_sp_municipios |
| tce_pe | buscar_despesas_pe | core | Pilot timed out; parameter names and pagination require a verified contract. |
| tce_pe | buscar_unidades_pe | lookup | Pilot loaded: tce_pe_unidades |
| tce_pi | consultar_despesas_pi | core | Pending implementation: verified query contract, identifiers and financial mapping. |
| tce_pi | buscar_prefeitura_pi | lookup | Pending implementation: verified query contract, identifiers and financial mapping. |
| tce_pi | listar_prefeituras_pi | lookup | Pilot loaded: tce_pi_prefeituras |
| tce_rn | buscar_despesas_rn | core | Parameterized route returned an empty array; jurisdiction and financial grain unverified. |
| tce_rn | listar_jurisdicionados_rn | lookup | Pending implementation: verified query contract, identifiers and financial mapping. |
| tce_ce | buscar_empenhos_ce | core | Catalog routes returned HTTP 404; replacement upstream contract required. |
| tce_ce | listar_municipios_ce | lookup | Pending implementation: verified query contract, identifiers and financial mapping. |
| tce_rs | buscar_gestao_fiscal_rs | core | Pending implementation: verified query contract, identifiers and financial mapping. |
| tce_rs | buscar_indices_educacao_rs | core | Pilot loaded: tce_rs_educacao |
| tce_rs | buscar_indices_saude_rs | core | Pending implementation: verified query contract, identifiers and financial mapping. |
| tce_rs | listar_municipios_rs | lookup | Pending implementation: verified query contract, identifiers and financial mapping. |

All 10 sources remain in scope. PI annual totals are a separately labeled supporting dataset and do not satisfy the detailed PI expense capability.
See [the runbook](runbooks/despesas-v1.md) for actual configured entities/periods and recovery commands.
