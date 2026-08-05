# Farol v1 — Fontes de dados sobre políticos

Escopo: responder qualquer pergunta sobre um parlamentar ou candidato —
o que propôs, como votou, quanto gastou, quem financiou, o que declarou ter,
o que a Justiça diz sobre ele, e para onde mandou dinheiro público.

Revisão de 03/08/2026. ⚠︎ = não revalidado endpoint a endpoint.

---

## Contexto de timing — isso importa

2026 é ano de eleição geral. O calendário está rodando **agora**:

- Convenções partidárias começaram em **20/07/2026**, prazo final **05/08**.
- Pedidos de registro de candidatura até **15/08/2026**.
- O DivulgaCandContas **já está recebendo e publicando** candidaturas de 2026.
- Prestação de contas parcial e o sistema IDC (Informações Durante a Campanha)
  publicam doações e gastos **durante** a campanha, não só depois.

Ou seja: se o Farol v1 estiver de pé em setembro/outubro, ele nasce com dado
fresco e relevância máxima. Se sair em novembro, nasce histórico. Isso deveria
pesar mais que qualquer decisão de arquitetura nas próximas semanas.

---

## 1. Identidade — a dimensão que amarra tudo

O problema central do v1 não é ingestão, é **entity resolution**. O mesmo
político aparece como `id` numérico na Câmara, `CodigoParlamentar` no Senado,
`SQ_CANDIDATO` no TSE (que **muda a cada eleição**), CPF no TSE e no Portal da
Transparência, e nome por extenso em tudo que é diário oficial.

| Fonte | O que dá | Acesso | URL |
|---|---|---|---|
| Câmara — `/deputados` | id, nome civil, nome eleitoral, CPF, partido, UF, legislatura | REST | dadosabertos.camara.leg.br/api/v2/deputados |
| Senado — parlamentares | CodigoParlamentar, nome, partido, UF, mandatos | REST/XML | dadosabertos.senado.leg.br |
| TSE — candidatos (bulk) | SQ_CANDIDATO, CPF, nome, cargo, situação, 2014–2024 | BULK | dadosabertos.tse.jus.br |
| TSE — DivulgaCandContas | Mesma informação para 2026, em tempo quase real | REST/Web | divulgacandcontas.tse.jus.br |
| Base dos Dados | Datasets TSE e Câmara já tratados e com chaves conciliadas | SQL/BULK | basedosdados.org |

**Estratégia:** CPF é a única chave estável entre TSE e Câmara/Senado. Modele
`dim_politico` com CPF como chave natural, `sq_candidato` como atributo
versionado por eleição, e uma tabela ponte `politico_id_externo` (fonte, id,
período de validade). Não tente uma chave única "esperta" — mantenha o mapa
explícito e auditável, porque você vai errar e vai precisar corrigir.

---

## 2. Atividade legislativa — "o que ele propôs e como votou"

| Fonte | O que tem | Acesso | URL |
|---|---|---|---|
| Câmara — proposições | PL/PEC/MP: ementa, temas, keywords, tramitação, relações entre proposições | REST + BULK anual | `/api/v2/proposicoes` · `dadosabertos.camara.leg.br/arquivos/proposicoesTemas` |
| Câmara — autores | Ponte proposição → autor. **Uma proposição tem N autores** (art. 102 do Regimento: quem assina é autor) — cuidado com fan-out na contagem | BULK | `/arquivos/proposicoesAutores` |
| Câmara — votações | Votações nominais, orientação de bancada, voto individual | REST | `/api/v2/votacoes` |
| Câmara — discursos | Pronunciamentos registrados por deputado | REST | `/api/v2/deputados/{id}/discursos` |
| Câmara — frentes e órgãos | Frentes parlamentares (bancadas temáticas), comissões, cargos | REST | `/api/v2/frentes` · `/api/v2/orgaos` |
| Câmara — eventos | Agenda de comissões, presenças | REST | `/api/v2/eventos` |
| Senado — matérias | Projetos, tramitação, relatorias | REST/XML | dadosabertos.senado.leg.br |
| Senado — votações | Votações nominais do plenário | REST/XML | dadosabertos.senado.leg.br |
| LexML | Norma final, quando o projeto vira lei | OAI-PMH | lexml.gov.br |
| DOU / Querido Diário | Nomeações, sanções, o que não aparece em API estruturada | REST | in.gov.br · queridodiario.ok.org.br |

**Nota de qualidade:** a API da Câmara pagina com máximo de 100 itens e retorna
`dados: []` (não 404) quando você pede página além do fim. Escreva o loop
esperando isso. Para carga histórica use os arquivos anuais, não a API.

---

## 3. Dinheiro do mandato — "quanto ele gasta"

| Fonte | O que tem | Acesso | URL |
|---|---|---|---|
| Câmara — CEAP (cota parlamentar) | Reembolsos e pagamentos por deputado: fornecedor, CNPJ, nota fiscal, valor líquido. **Série desde 2008**, arquivos anuais, atualização diária | BULK | `camara.leg.br/cotas/Ano-{ano}.{formato}.zip` |
| Câmara — CEAP via API | Mesmo dado por deputado, últimos anos | REST | `/api/v2/deputados/{id}/despesas` |
| Senado — CEAPS | Equivalente do Senado, em CSV | BULK | senado.leg.br/transparencia |
| Câmara — verba de gabinete | Secretários parlamentares, folha do gabinete ⚠︎ | BULK | camara.leg.br/transparencia |
| Portal da Transparência — SIAPE | Remuneração de servidores, inclusive comissionados de gabinete | REST 🔑 / BULK | portaldatransparencia.gov.br |

**Duas armadilhas conhecidas** (ambas geram manchete errada se ignoradas):

1. Os arquivos de cota **não seguem o mesmo padrão de nomenclatura e
   identificadores** do resto do portal da Câmara. Layout próprio, dicionário
   próprio.
2. O deputado tem **90 dias** para apresentar o comprovante, e a despesa é
   debitada no mês de referência. Ou seja: o total dos últimos 3 meses está
   sempre subestimado. Qualquer ranking de "quem gastou mais" precisa de uma
   janela de corte, ou você publica um número que muda sozinho.

---

## 4. Emendas parlamentares — "para onde ele manda dinheiro"

Esta é a seção com maior densidade de história por linha de código, e a que
mudou mais recentemente.

| Fonte | O que tem | Acesso | URL |
|---|---|---|---|
| Portal da Transparência — Emendas | Emenda → autor → favorecido → empenho → pagamento, já integrado com convênios | REST 🔑 / BULK | portaldatransparencia.gov.br/emendas · download-de-dados/emendas-parlamentares |
| TransfereGov — Transferências Especiais | API de dados abertos das emendas PIX (EC 105/2019). **PostgREST** — filtros no padrão `campo=eq.valor`, o que é ótimo para ingestão | REST | docs.api.transferegov.gestao.gov.br/transferenciasespeciais |
| SIOP — emendas | Orçamento marcado por RP6 (individual, desde 2014) e RP7 (bancada, desde 2017). É a origem orçamentária | BULK/REST | siop.planejamento.gov.br |
| Tesouro Transparente | Painel de emendas individuais e de bancada | BULK | tesourotransparente.gov.br |
| TransfereGov — convênios | Prestação de contas do que foi executado | REST | api.transferegov.gestao.gov.br |

**Novidade de maio/2026:** a CGU integrou ao Portal da Transparência o
detalhamento das emendas "Individual – Transferências Especiais" — objeto,
plano de trabalho, relatório de gestão e **extrato bancário**, puxando direto do
Transferegov. São R$ 30,5 bilhões com rastro até o extrato. Isso é novo o
suficiente para que quase ninguém tenha modelado ainda.

**Cuidado com a consulta web:** o download pela interface é limitado a 20.000
registros. Use o arquivo completo em "Dados abertos", não a consulta filtrada.

---

## 5. Campanha e patrimônio — "quem o financia e o que ele tem"

| Fonte | O que tem | Acesso | URL |
|---|---|---|---|
| TSE — DivulgaCandContas | Por candidato: registro (deferido/indeferido), **declaração de bens item a item**, proposta de governo, arrecadação, limite de gastos, doadores, fornecedores, financiamento coletivo, sobras e dívidas | REST/Web | divulgacandcontas.tse.jus.br |
| TSE — Dados Abertos: prestação de contas | Receitas e despesas de candidatos, partidos e comitês, em bulk por eleição | BULK | dadosabertos.tse.jus.br/group/prestacao-de-contas-eleitorais |
| TSE — bens de candidatos | Patrimônio declarado, série 2014–2024, join por `sq_candidato` | BULK | dadosabertos.tse.jus.br |
| TSE — FEFC | Distribuição do fundo eleitoral por partido e candidato | BULK | dadosabertos.tse.jus.br |
| TSE — resultados | Votação por município e zona | REST/CDN | resultados.tse.jus.br |
| TSE — CNPJ de campanha | Lista de CNPJs atribuídos a candidatos e partidos em 2026 ⚠︎ | BULK | tse.jus.br/eleicoes/eleicoes-2026 |
| Meta Ad Library | Anúncios políticos veiculados, com gasto e alcance | REST 🔑 | facebook.com/ads/library/api |

**A pergunta que vende o projeto:** evolução patrimonial declarada entre
eleições, cruzada com renda de mandato. É um join simples (bens 2018 × bens 2022
× bens 2026 por CPF) e é exatamente o tipo de coisa que ninguém consegue fazer
manualmente. Cuidado com inflação — normalize por IPCA (série do BCB/SGS) antes
de afirmar "cresceu X%".

**O CNPJ de campanha é uma chave subestimada.** Ele conecta prestação de contas
eleitoral com a base da Receita, e daí com contratos públicos.

---

## 6. Antecedentes e controle — "o que pesa contra ele"

| Fonte | O que tem | Acesso | URL |
|---|---|---|---|
| CGU — sanções (CEIS/CNEP/CEPIM/CEAF) | Empresas e pessoas sancionadas. CEAF = expulsões de servidores | REST 🔑 / BULK | portaldatransparencia.gov.br |
| TCU | Inidôneos, contas irregulares, acórdãos, CADIRREG | REST | dados-abertos.apps.tcu.gov.br |
| DataJud / CNJ | Processos e movimentações em todos os tribunais | REST 🔑 | api-publica.datajud.cnj.jus.br |
| STF | Ações penais e inquéritos de foro privilegiado, jurisprudência | REST | portal.stf.jus.br |
| TSE — situação do registro | Indeferimento, Ficha Limpa (Lei Complementar 135) | REST | divulgacandcontas.tse.jus.br |
| Lista Suja (trabalho escravo) | Empregadores autuados — relevante quando o político é sócio ⚠︎ | BULK | gov.br/trabalho |

**Aqui é onde o projeto pode se destruir.** Uma condenação em primeira instância
não é uma condenação transitada em julgado; um inquérito não é uma acusação; um
homônimo no DataJud não é a mesma pessoa. Modele `status_processual` e
`instancia` como campos de primeira classe e **nunca** exponha um agregado do
tipo "N processos" sem essa qualificação. O dano reputacional de um falso
positivo aqui é assimétrico e irreversível.

---

## 7. Vínculos econômicos — "com quem ele se relaciona"

| Fonte | O que tem | Acesso | URL |
|---|---|---|---|
| RFB — CNPJ | Sócios e administradores (~60M empresas). Permite: político → empresas onde é sócio → contratos públicos dessas empresas | BULK (~20 GB) | gov.br/receitafederal |
| PNCP / Compras.gov.br | Contratos e licitações dos fornecedores identificados | REST/BULK | pncp.gov.br · dadosabertos.compras.gov.br |
| Contratos.gov.br | Empenhos, faturas e aditivos federais pós-2021 | REST | contratos.comprasnet.gov.br/api |
| SIORG | Estrutura de órgãos — para nomeações e indicações políticas | REST | api.siorg.gov.br |

O grafo `político → CPF de sócio → CNPJ → contrato público` é o ativo diferencial
do Farol. Ninguém oferece isso pronto e é puro trabalho de engenharia de dados,
que é exatamente o que você quer demonstrar.

---

## 8. Prior art — leia antes de construir

Não para copiar, para não repetir erro e para saber onde o diferencial está.

| Projeto | O que faz | Por que importa |
|---|---|---|
| Operação Serenata de Amor / Rosie | ML sobre a CEAP para achar reembolso suspeito | Referência canônica em cota parlamentar. Já resolveu boa parte da limpeza |
| Jarbas | Interface de exploração dos reembolsos da Serenata | Mostra o que funciona em UX de auditoria |
| Parlametria / Radar Parlamentar | Análise de convergência de voto entre parlamentares | Boa modelagem de votação nominal |
| Base dos Dados | TSE e Câmara já tratados no BigQuery | Use como fonte de verdade para validar sua própria ingestão |
| Querido Diário (Open Knowledge Brasil) | Diários municipais em full-text | Modelo de governança de projeto cívico open source |

O que nenhum deles faz bem: **unificar as camadas**. Serenata só olha cota;
Parlametria só olha voto; Base dos Dados entrega tabela, não resposta. O Farol
como camada de pergunta em linguagem natural sobre o grafo inteiro — mandato +
gasto + emenda + campanha + patrimônio + vínculo empresarial — é território
vago.

---

## Sequência sugerida do v1

1. `dim_politico` + ponte de ids (Câmara, Senado, TSE) — sem isso nada cruza
2. CEAP bulk 2008–2026 + fornecedores por CNPJ — o dataset mais limpo e mais
   imediatamente interessante
3. Proposições, autores e votações — dá o "o que ele defende"
4. Emendas via Portal da Transparência + TransfereGov — o dinheiro grande
5. TSE: candidaturas 2026, bens, doadores — aproveitando a janela eleitoral
6. RFB CNPJ + o grafo de vínculos — o diferencial
7. Camada de agente / MCP por cima

Passos 1–3 já respondem uma quantidade absurda de pergunta e cabem em semanas,
não meses.

---

## Nota de responsabilidade

Políticos e candidatos são figuras públicas e seus dados de mandato, campanha e
patrimônio declarado são públicos por lei. Isso **não** se estende a:

- **CPF de doadores pessoa física** e de terceiros que aparecem nas bases do TSE
  e do Portal da Transparência — mascare na ingestão
- **Familiares** que aparecem em declaração de bens ou em quadro societário sem
  serem eles próprios agentes públicos
- **Homônimos** no DataJud e nas listas de sanção

E a regra que decide a credibilidade do projeto: **toda afirmação exibida deve
carregar fonte, data de extração e URL de origem**. Um número sem procedência é
indistinguível de desinformação, mesmo quando está certo. Guarde
`source_url`, `extracted_at` e `source_version` na landing zone e propague até a
camada de apresentação.