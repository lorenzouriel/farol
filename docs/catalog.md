# Catálogo de APIs e Dados Públicos do Brasil — v2

Revisão de 30/07/2026. Organizado por área temática, com o padrão de ingestão de
cada fonte — que é o que decide se ela entra no lakehouse por batch, por API
paginada ou por download bulk.

**Legenda de acesso**
- `REST` — API REST/JSON, boa para consulta pontual, ruim para volume
- `BULK` — CSV/ZIP/Parquet para download, é o que você quer para carga histórica
- `CKAN` — portal CKAN (catálogo + datastore), API padronizada
- `OGC` — geoserviço WMS/WFS/WCS ou REST ArcGIS
- `SOAP` — serviço legado
- 🔑 — exige chave/cadastro
- ⚠︎ — entrada nova, **não revalidada endpoint a endpoint** nesta revisão

> As URLs de portais governamentais brasileiros mudam com frequência e vários
> endpoints têm documentação incompleta. Valide antes de codificar contra eles.

---

## Changelog v1 → v2

**Validado e mantido**
- PNCP — `pncp.gov.br/api/consulta/swagger-ui/index.html` continua ativo. Só as
  APIs de *manutenção* (inserção/retificação) exigem credenciamento; a API de
  consulta é pública e sem token. O ambiente `treina.pncp.gov.br` existe e serve
  para teste de integração.
- mcp-brasil — confirmado: ~70 fontes, 533 tools, 15 áreas temáticas, com
  ingestão de bulk pesado (TSE, SPU/SIAPA) para DuckDB embarcado. Como
  referência estrutural o mapeamento continua bom.

**Corrigido**
- **ANM mudou de endereço** (05/02/2026): os dados abertos agora ficam em
  `dadosabertos.anm.gov.br`. O endereço antigo só responde até **30/06/2026** —
  ou seja, já morreu. SIGMINE publica `BRASIL.zip` (~125 MB) e um shapefile/KMZ
  por UF, regenerados **diariamente**.
- **Portal da Transparência** — não é mais "cadastro de e-mail". O token sai de
  conta gov.br nível **Prata ou Ouro** (ou CPF/senha com 2FA) e chega por
  e-mail. Rate limit **varia por faixa horária** — 700 req/min entre 00:00 e
  06:00, e bem menos no horário comercial. Isso muda a janela de ingestão.

**Lacunas fechadas** (o que faltava na v1)
Ciência e inovação · Terra e cadastro rural · Mineração e geologia · Camada
geoespacial transversal (INDE/OGC) · Assistência social e CadÚnico · Estado,
orçamento e servidores · Registro civil e demografia · Cultura, turismo e
esporte · Portais estaduais e municipais · Bibliotecas cliente.

Fontes pontuais relevantes que faltavam e entram nas seções existentes: **PGFN
Dívida Ativa**, **CMED/ANVISA (preço máximo de medicamentos)**, **SIGTAP**,
**PRF (acidentes)**, **Lista Suja do trabalho escravo**, **SIORG**,
**servicos.gov.br**.

---

## 1. Catálogos e meta-fontes

Comece por aqui antes de sair caçando endpoint por endpoint.

| Fonte | O que tem | Acesso | URL |
|---|---|---|---|
| Portal Brasileiro de Dados Abertos | Catálogo central do governo federal | CKAN 🔑 | dados.gov.br |
| Catálogo Conecta gov.br | APIs de interoperabilidade entre órgãos | REST 🔑 | gov.br/conecta/catalogo |
| catalogos-dados-brasil | Levantamento de portais de dados abertos estaduais e municipais | BULK (repo) | github.com/dadosgovbr/catalogos-dados-brasil |
| servicos.gov.br | Catálogo de serviços públicos federais, com API própria ⚠︎ | REST | servicos.gov.br/api/v1/servicos |
| Base dos Dados | Datasets públicos já tratados no BigQuery | SQL/BULK | basedosdados.org |
| Querido Diário | Diários oficiais de 5.000+ municípios, full-text | REST | queridodiario.ok.org.br |
| Imprensa Nacional / DOU | Diário Oficial da União | REST | in.gov.br |
| Ro-dou (MGI) | DAGs Airflow prontas para clipping do DOU | Código | github.com/gestaogovbr/Ro-dou |
| mcp-brasil | Servidor MCP agregando ~70 fontes oficiais | MCP | github.com/Mcp-Brasil/mcp-brasil |

---

## 2. Economia, finanças e cadastro empresarial

| Fonte | O que tem | Acesso | URL |
|---|---|---|---|
| BCB / SGS | +190 séries: Selic, IPCA, câmbio, PIB, crédito | REST | dadosabertos.bcb.gov.br |
| BCB / Olinda | Expectativas Focus, PIX, Open Finance, IF.data | REST (OData) | olinda.bcb.gov.br |
| IBGE — servicodados | Municípios, estados, CNAE, malhas GeoJSON, nomes | REST | servicodados.ibge.gov.br/api/docs |
| IBGE — SIDRA | Agregados de todas as pesquisas (PNAD, PIB, IPCA, censo) | REST/BULK | apisidra.ibge.gov.br |
| Receita Federal — CNPJ | ~60M empresas: empresa, estabelecimento, sócios, Simples | BULK (~20 GB) | gov.br/receitafederal → dados públicos CNPJ |
| **PGFN — Dívida Ativa da União** | Devedores da União, FGTS e previdenciária, por CPF/CNPJ ⚠︎ | BULK | dadosabertos.pgfn.gov.br |
| Tesouro Transparente / SICONFI | Finanças de estados e municípios, RREO, RGF, dívida | REST/BULK | apidatalake.tesouro.gov.br |
| **Tesouro Direto** | Preços e taxas históricos dos títulos públicos ⚠︎ | BULK | tesourotransparente.gov.br |
| Comex Stat | Exportação e importação por NCM, município, país | BULK | comexstat.mdic.gov.br |
| CVM | Dados cadastrais e demonstrativos de companhias e fundos | BULK | dados.cvm.gov.br |
| **SUSEP** | Mercado segurador: prêmios, sinistros, operadoras (SES / PIMS) | BULK | www2.susep.gov.br → estatísticas |
| **PREVIC** | Fundos de pensão / entidades fechadas ⚠︎ | BULK | gov.br/previc |
| BNDES | Operações de financiamento, desembolsos, credenciadas | CKAN | dadosabertos.bndes.gov.br |
| IPEA / Ipeadata | Séries macroeconômicas, regionais e sociais | REST | ipeadata.gov.br |

---

## 3. Compras públicas e contratos

O núcleo do projeto de detecção de sobrepreço. PNCP é o portal oficial pós-Lei
14.133 e agrega União, estados e municípios; Compras.gov.br é federal e traz o
item-level com código de catálogo.

| Fonte | O que tem | Acesso | URL |
|---|---|---|---|
| PNCP | Contratações, contratos, atas de registro de preço, PCA | REST | pncp.gov.br/api/consulta/swagger-ui |
| PNCP — treina | Ambiente de homologação para testar integração | REST | treina.pncp.gov.br |
| Compras.gov.br — Dados Abertos | SIASG + Compras.gov, itens, resultados, fornecedores | REST | dadosabertos.compras.gov.br |
| Compras.gov.br — Repositório CSV | Views tipo fato/dimensão anuais (compra, item, resultado) | BULK | repositorio.dados.gov.br/seges/comprasgov |
| Contratos.gov.br | Contratos federais pós-2021: empenhos, faturas, aditivos | REST | contratos.comprasnet.gov.br/api |
| CATMAT / CATSER | Catálogo federal de materiais e serviços | REST | via API Compras |
| **SICAF** | Cadastro de fornecedores, situação e ocorrências ⚠︎ | REST | via API Compras |
| Banco de Preços em Saúde (BPS) | Preços de medicamentos e insumos comprados pelo governo | REST | bps.saude.gov.br |
| **CMED / ANVISA** | Preço máximo ao consumidor e ao governo (PMVG) por medicamento — teto legal, essencial para flag de sobrepreço ⚠︎ | BULK | gov.br/anvisa → CMED listas de preços |
| **SIGTAP** | Tabela de procedimentos, medicamentos e OPM do SUS, com valores de referência ⚠︎ | BULK/REST | sigtap.datasus.gov.br |
| Painel de Preços | Referência de preços praticados em compras federais | Web/REST | paineldeprecos.planejamento.gov.br |

---

## 4. Transparência e controle

| Fonte | O que tem | Acesso | URL |
|---|---|---|---|
| Portal da Transparência (CGU) | Contratos, despesas, servidores, sanções (CEIS/CNEP/CEPIM/CEAF), Bolsa Família, emendas, cartões, convênios, viagens | REST 🔑 gov.br Prata/Ouro | api.portaldatransparencia.gov.br |
| Portal da Transparência — download | Mesmas bases em CSV mensal, sem token e sem rate limit | BULK | portaldatransparencia.gov.br/download-de-dados |
| TCU | Acórdãos, inidôneos, inabilitados, certidões, CADIRREG | REST | dados-abertos.apps.tcu.gov.br |
| TransfereGov | Emendas PIX / transferências especiais, convênios | REST | api.transferegov.gestao.gov.br |
| **Fala.BR / e-SIC** | Pedidos e recursos de acesso à informação (LAI), com respostas ⚠︎ | BULK | falabr.cgu.gov.br |
| Tribunais de Contas Estaduais | Licitações, contratos, obras, despesas por UF (SP, RJ, RS, SC, PE, CE, RN, PI, TO, ES, PA…) | REST | varia por TCE |
| SPU / Patrimônio da União | ~813k imóveis da União, terrenos de marinha | BULK | patrimoniodetodos.gov.br |

---

## 5. Estado, orçamento e servidores — **nova**

| Fonte | O que tem | Acesso | URL |
|---|---|---|---|
| **SIORG** | Estrutura organizacional do governo federal: órgãos, unidades, hierarquia, cargos — a dimensão órgão que amarra despesa, compra e servidor ⚠︎ | REST | api.siorg.gov.br (swagger em github.com/gestaogovbr) |
| **SIOP** | Orçamento federal: LOA, dotação, execução por ação e programa ⚠︎ | BULK/REST | siop.planejamento.gov.br |
| **SIGA Brasil (Senado)** | Painel/base do orçamento federal, série longa ⚠︎ | BULK | senado.leg.br/orcamento |
| **SIAPE (via Transparência)** | Servidores federais, remuneração, cargo, lotação | REST/BULK | portaldatransparencia.gov.br |
| **Consumidor.gov.br** | Reclamações registradas contra empresas ⚠︎ | BULK | consumidor.gov.br → dados abertos |

---

## 6. Legislativo

| Fonte | O que tem | Acesso | URL |
|---|---|---|---|
| Câmara dos Deputados | Deputados, proposições, votações nominais, despesas (cota parlamentar), comissões, frentes | REST | dadosabertos.camara.leg.br |
| Senado Federal | Senadores, matérias, votações, comissões, agenda, lideranças | REST/XML | dadosabertos.senado.leg.br |
| LexML | Rede de normas jurídicas federais, estaduais e municipais | OAI-PMH | lexml.gov.br |
| Planalto | Legislação federal consolidada | Scrape | planalto.gov.br |

---

## 7. Judiciário

| Fonte | O que tem | Acesso | URL |
|---|---|---|---|
| DataJud / CNJ | Processos de todos os tribunais, movimentações | REST 🔑 grátis | api-publica.datajud.cnj.jus.br |
| STF | Jurisprudência, repercussão geral, informativos | REST | portal.stf.jus.br |
| STJ | Jurisprudência, súmulas | REST | scon.stj.jus.br |
| TST | Jurisprudência trabalhista | REST | tst.jus.br |
| CNJ — Painéis | Produtividade, Justiça em Números | BULK | cnj.jus.br/dadosabertos |

---

## 8. Eleitoral

| Fonte | O que tem | Acesso | URL |
|---|---|---|---|
| TSE — Divulgação de Candidaturas | Candidatos, bens declarados, prestação de contas, coligações | REST/BULK | divulgacandcontas.tse.jus.br |
| TSE — Resultados | Apuração por município e zona, resultados históricos | REST/CDN | resultados.tse.jus.br |
| TSE — Dados Abertos | Candidatos e votação 2014–2024, FEFC, redes sociais (bulk pesado, ~1,6 GB na votação) | BULK | dadosabertos.tse.jus.br |
| Meta Ad Library | Anúncios eleitorais e políticos veiculados no Brasil | REST 🔑 | facebook.com/ads/library/api |

---

## 9. Saúde

| Fonte | O que tem | Acesso | URL |
|---|---|---|---|
| CNES / DataSUS | Estabelecimentos, profissionais, leitos, equipamentos | REST/BULK | cnes.datasus.gov.br |
| OpenDataSUS | Vacinação, SRAG, notificações, qualidade da água | CKAN | opendatasus.saude.gov.br |
| DataSUS — SIH/SIA/SIM/SINASC | Internações, produção ambulatorial, mortalidade, nascimentos (bilhões de linhas históricas, formato DBC) | BULK (FTP) | datasus.gov.br → TabNet / arquivos |
| **SISAB / e-SUS APS** | Produção da atenção primária por município e equipe ⚠︎ | BULK | sisab.saude.gov.br |
| ANVISA | Bulário eletrônico, registros, medicamentos, empresas | REST | consultas.anvisa.gov.br |
| ANS | Operadoras, beneficiários, ressarcimento ao SUS | BULK | dadosabertos.ans.gov.br |
| SIGTAP | Procedimentos e valores de referência do SUS ⚠︎ | BULK | sigtap.datasus.gov.br |
| RENAME | Relação Nacional de Medicamentos Essenciais | REST | via SUS |
| Farmácia Popular | Farmácias credenciadas, medicamentos gratuitos | REST | via SUS |
| PNI / Imunizações | Doses aplicadas, cobertura vacinal | CKAN | via OpenDataSUS |
| DENASUS | Auditorias do SUS por município | REST | via SUS |

---

## 10. Educação

| Fonte | O que tem | Acesso | URL |
|---|---|---|---|
| INEP — Censo Escolar | Escolas, matrículas, docentes, turmas (microdados anuais) | BULK | gov.br/inep → microdados |
| INEP — ENEM | Microdados por participante, notas, socioeconômico | BULK | gov.br/inep → microdados |
| **INEP — Censo da Educação Superior / ENADE** | Matrículas, cursos e desempenho no ensino superior ⚠︎ | BULK | gov.br/inep → microdados |
| INEP — IDEB / SAEB | Indicadores de qualidade por escola e município | BULK | gov.br/inep |
| FNDE | Repasses, PNAE, PNATE, transferências a municípios | REST/BULK | fnde.gov.br/dadosabertos |
| **SIMEC / Obras** | Obras da educação: status, valor, atraso ⚠︎ | BULK | simec.mec.gov.br |
| e-MEC | Instituições e cursos de ensino superior | REST | emec.mec.gov.br |

---

## 11. Ciência, tecnologia e inovação — **nova**

| Fonte | O que tem | Acesso | URL |
|---|---|---|---|
| CNPq — Dados Abertos | Bolsas e auxílios pagos (por beneficiário e instituição), séries de fomento, Painel Lattes | BULK | memoria.cnpq.br/web/guest/dados_abertos |
| CNPq — Diretório de Grupos de Pesquisa (DGP) | Grupos, linhas de pesquisa, integrantes | BULK/REST | lattes.cnpq.br/web/dgp |
| Plataforma Lattes | Currículos de pesquisadores — sem API aberta oficial; acesso via extrações do CNPq e projetos derivados | Restrito | lattes.cnpq.br |
| CAPES — Dados Abertos | Pós-graduação: programas, discentes, docentes, bolsas no país e no exterior, PROAP/PROEX | CKAN | dadosabertos.capes.gov.br |
| **INPI — Dados Abertos** | Marcas, patentes, desenhos industriais, programas de computador e contratos de transferência de tecnologia. **Abertos em fev/2026**, portanto ainda pouco explorados | BULK | gov.br/inpi → acesso à informação → dados abertos |
| IBICT / BrCris / BDTD | Teses, dissertações, produção científica agregada ⚠︎ | OAI-PMH/REST | brcris.ibict.br · bdtd.ibict.br |
| FINEP | Projetos financiados, chamadas ⚠︎ | BULK | finep.gov.br |

---

## 12. Terra, cadastro rural e territórios — **nova**

| Fonte | O que tem | Acesso | URL |
|---|---|---|---|
| SICAR / CAR | Cadastro Ambiental Rural: polígonos de imóveis, APP, reserva legal. Download por município, **com captcha** — não é scriptável direto | BULK | car.gov.br |
| MapBiomas — espelho do CAR | Mesmos polígonos servidos por WMS/download, sem captcha (mais desatualizado, menos atributos) | OGC/BULK | mapbiomas.org |
| INCRA — Acervo Fundiário | Imóveis certificados (SIGEF e SNCI), assentamentos, territórios quilombolas. Shapefile + WMS/WFS | OGC/BULK 🔑 gov.br | acervofundiario.incra.gov.br |
| INCRA — SIGEF | Parcelas georreferenciadas certificadas; API restrita a órgãos públicos federais/estaduais | REST 🔑 | via Conecta gov.br |
| INCRA — SNCR | Relação de imóveis rurais cadastrados, com CPF/nome anonimizados, licença ODbL | BULK | dados.gov.br → SNCR |
| **FUNAI** | Terras indígenas: limites, fases do processo demarcatório ⚠︎ | OGC/BULK | funai.gov.br → geoprocessamento |
| **ICMBio / CNUC** | Unidades de conservação federais e estaduais ⚠︎ | OGC/BULK | icmbio.gov.br · cnuc.mma.gov.br |

---

## 13. Mineração e geologia — **nova**

| Fonte | O que tem | Acesso | URL |
|---|---|---|---|
| ANM — Dados Abertos | Processos minerários, arrecadação CFEM, TAH, produção (RAL). **Endereço novo desde fev/2026** | BULK | dadosabertos.anm.gov.br |
| ANM — SIGMINE | Poligonais de processos ativos/inativos, bloqueio, reservas garimpeiras. `BRASIL.zip` (~125 MB) + por UF, regerado diariamente | BULK (SHP/KMZ) | dadosabertos.anm.gov.br/SIGMINE |
| ANM — SIGBM | Barragens de mineração: cadastro, nível de risco, dano potencial | BULK | dados.gov.br → barragens-de-mineracao |
| ANM — GeoServices | Camadas ArcGIS REST | OGC | geo.anm.gov.br/arcgis/rest/services |
| SGB / CPRM — GeoSGB | Geologia, recursos minerais, hidrogeologia, RIMAS | OGC/BULK | geoportal.sgb.gov.br/server/rest/services |

---

## 14. Meio ambiente e clima

| Fonte | O que tem | Acesso | URL |
|---|---|---|---|
| INPE — Queimadas | Focos ativos de incêndio, série histórica | REST/BULK | terrabrasilis.dpi.inpe.br |
| INPE — PRODES / DETER | Desmatamento consolidado e alertas | REST/BULK | terrabrasilis.dpi.inpe.br |
| INPE — CPTEC | Previsão do tempo, modelos numéricos | REST/XML | cptec.inpe.br |
| INMET | Estações meteorológicas, séries horárias, normais | REST/BULK | portal.inmet.gov.br |
| ANA / SNIRH | Estações hidrológicas, telemetria (chuva, vazão, nível), reservatórios | REST/OGC | dadosabertos.ana.gov.br · wms.snirh.gov.br |
| CEMADEN | Alertas e pluviômetros de risco de desastre | REST | cemaden.gov.br |
| IBAMA | Autuações, embargos, licenças | BULK | dadosabertos.ibama.gov.br |
| IBAMA — PAMGIA | Camadas geoespaciais ambientais (embargos, autuações georreferenciadas) | OGC | pamgia.ibama.gov.br/server/rest/services |
| MMA — i3Geo | Acervo geoespacial ambiental | OGC/BULK | mapas.mma.gov.br/i3geo |
| MapBiomas | Uso e cobertura do solo, alertas de desmatamento | BULK/GEE | mapbiomas.org |
| Marinha — Tábua de Marés | Previsão de marés dos portos brasileiros | REST | marinha.mil.br/chm |

---

## 15. Camada geoespacial transversal — **nova**

Não é um domínio: é a malha que amarra todos os outros. Trate como camada de
dimensões espaciais conformadas, não como uma seção paralela.

| Fonte | O que tem | Acesso | URL |
|---|---|---|---|
| INDE — Catálogo de Geoserviços | Índice federado de WMS/WFS de órgãos federais, estaduais e municipais. Ponto de partida antes de caçar geoserviço por órgão | OGC (catálogo) | inde.gov.br/CatalogoGeoservicos |
| INDE — Visualizador | Cliente web, útil para inspeção rápida de camada | Web | visualizador.inde.gov.br |
| IBGE — Downloads Geociências | Malhas municipais/estaduais, setores censitários, BC250, relevo | BULK | ibge.gov.br/geociencias/downloads-geociencias.html |
| IBGE — geoftp | Mesmo acervo por FTP, melhor para automação | FTP/BULK | geoftp.ibge.gov.br |
| DNIT — VGeo | Malha rodoviária federal, SNV, obras | OGC | servicos.dnit.gov.br/vgeo |

---

## 16. Energia e combustíveis

| Fonte | O que tem | Acesso | URL |
|---|---|---|---|
| ANEEL | Geração, tarifas, capacidade instalada, geração distribuída | CKAN | dadosabertos.aneel.gov.br |
| ONS | Carga, geração, reservatórios, restrições — série horária | REST/BULK | dados.ons.org.br |
| CCEE | Preço de liquidação (PLD), contabilização do mercado | REST/BULK | ccee.org.br |
| ANP | Preços de combustíveis por posto, produção de petróleo e gás | BULK | gov.br/anp → dados abertos |
| EPE | Balanço energético nacional, projeções | BULK | epe.gov.br |

---

## 17. Transporte e mobilidade

| Fonte | O que tem | Acesso | URL |
|---|---|---|---|
| ANTT | Concessões rodoviárias, transporte interestadual, fretes | CKAN | dados.antt.gov.br |
| ANAC | Voos regulares, aeronaves, tarifas aéreas, ocorrências | BULK | gov.br/anac → dados abertos |
| ANTAQ | Movimentação portuária, cargas, navegação | BULK | web.antaq.gov.br |
| DNIT | Malha rodoviária federal, PNV/SNV, obras | BULK/OGC | dnit.gov.br · servicos.dnit.gov.br/vgeo |
| **PRF — Acidentes** | Acidentes em rodovias federais, por ocorrência e por pessoa, série desde 2007. Um dos datasets públicos mais limpos do país ⚠︎ | BULK | gov.br/prf → dados abertos |
| SENATRAN / RENAVAM | Frota por município, tipo e combustível; infrações | BULK | gov.br/transportes |
| GTFS municipais | Rotas e horários de transporte público (SP, RJ, BH, POA…) | BULK | varia por cidade |

---

## 18. Trabalho, previdência e assistência social

| Fonte | O que tem | Acesso | URL |
|---|---|---|---|
| Novo CAGED | Admissões e desligamentos mensais por município e CNAE | BULK (FTP) | pdet.mte.gov.br |
| RAIS | Vínculos formais, remuneração, perfil (microdados anuais) | BULK (FTP) | pdet.mte.gov.br |
| **Cadastro de Empregadores (Lista Suja)** | Empregadores autuados por trabalho análogo ao escravo ⚠︎ | BULK | gov.br/trabalho |
| INSS / Dataprev | Benefícios concedidos, estatísticas previdenciárias | BULK | dataprev.gov.br |
| eSocial | Layouts e tabelas de referência | BULK | gov.br/esocial |
| **CadÚnico — microdados amostrais** | Amostra desidentificada: 30 variáveis de família, 34 de pessoa | BULK | dados.gov.br → microdados-amostrais-do-cadastro-unico |
| **MDS / SAGI — VIS DATA e CECAD** | Agregados de CadÚnico, Bolsa Família e BPC por município, série mensal | Web/BULK | aplicacoes.mds.gov.br/sagi |
| **CadÚnico Serviços (Conecta)** | API de consulta cadastral — restrita a órgãos | REST 🔑 | gov.br/conecta/catalogo/apis/cadunico-servicos |

---

## 19. Segurança pública

| Fonte | O que tem | Acesso | URL |
|---|---|---|---|
| SINESP / MJSP | Ocorrências criminais, sistema prisional (SISDEPEN) | CKAN | dados.mj.gov.br |
| Atlas da Violência (IPEA) | Homicídios, violência por gênero e raça, séries históricas | REST | ipea.gov.br/atlasviolencia |
| Fórum Brasileiro de Segurança Pública | Anuário, publicações, microdados | DSpace | forumseguranca.org.br |
| ISP-RJ | Estatísticas criminais do Rio de Janeiro | BULK | isp.rj.gov.br |
| SSP-SP | Boletins de ocorrência agregados de São Paulo | BULK | ssp.sp.gov.br |

---

## 20. Agropecuária e abastecimento

| Fonte | O que tem | Acesso | URL |
|---|---|---|---|
| CONAB | Safras, estoques, preços agrícolas | BULK | conab.gov.br |
| MAPA | Agrotóxicos registrados, estabelecimentos, SIF | BULK | gov.br/agricultura |
| EMBRAPA | Dados agrometeorológicos e de pesquisa | REST/BULK | embrapa.br |
| IBGE — PAM / PPM / LSPA | Produção agrícola e pecuária municipal | REST (SIDRA) | apisidra.ibge.gov.br |

---

## 21. Cultura, turismo e esporte — **nova**

| Fonte | O que tem | Acesso | URL |
|---|---|---|---|
| **SALIC / Lei Rouanet** | Projetos culturais incentivados: proponente, valor captado, execução — tem API pública ⚠︎ | REST | api.salic.cultura.gov.br |
| **IPHAN** | Bens tombados, sítios arqueológicos (SICG) ⚠︎ | OGC/BULK | iphan.gov.br |
| **Ministério do Turismo / Embratur** | Chegadas de turistas, Cadastur (prestadores cadastrados) ⚠︎ | BULK | dados.turismo.gov.br |
| **Loterias Caixa** | Resultados de todos os concursos, com API pública ⚠︎ | REST | servicebus2.caixa.gov.br/portaldeloterias/api |

---

## 22. Telecom e infraestrutura urbana

| Fonte | O que tem | Acesso | URL |
|---|---|---|---|
| ANATEL | Acessos por município e tecnologia, cobertura, reclamações | CKAN | dadosabertos.anatel.gov.br |
| Correios | CEP, agências, cálculo de frete e prazo | REST/SOAP 🔑 | correios.com.br |
| SNIS / SINISA | Saneamento: água, esgoto, resíduos por município | BULK | snis.gov.br |

---

## 23. Registro civil e demografia — **nova**

| Fonte | O que tem | Acesso | URL |
|---|---|---|---|
| ARPEN — Transparência Registro Civil | Nascimentos, casamentos e óbitos registrados em cartório, com latência de dias. Fecha o gap do SIM/SINASC, que atrasa anos | REST/Web | transparencia.registrocivil.org.br |
| IBGE — Censo 2022 | Agregados por setor censitário, população, domicílios | REST (SIDRA) / BULK | apisidra.ibge.gov.br |
| IBGE — Projeções e Estimativas | População estimada por município, ano a ano — denominador de qualquer taxa per capita | REST | servicodados.ibge.gov.br |

---

## 24. Utilidades e identificadores

| Fonte | O que tem | Acesso | URL |
|---|---|---|---|
| BrasilAPI | CEP, CNPJ, DDD, bancos, FIPE, feriados, PIX, ISBN, NCM, registro.br | REST | brasilapi.com.br |
| ViaCEP | Consulta de CEP | REST | viacep.com.br |
| ReceitaWS / CNPJá / Casa dos Dados | CNPJ enriquecido (limites em plano free) | REST 🔑 | vários |
| FIPE | Tabela de preços de veículos | REST | via BrasilAPI |
| SERPRO | CPF, CNPJ, NF-e, Datavalid (comercial) | REST 🔑 pago | serpro.gov.br |

---

## 25. Estados e municípios — **nova**

Não dá para enumerar 5.570 municípios. O caminho é meta-fonte + padrão.

- **catalogos-dados-brasil** (`github.com/dadosgovbr/catalogos-dados-brasil`) —
  levantamento dos portais de transparência e dados abertos estaduais e
  municipais. Use como seed list.
- **CKAN é o padrão de fato** nos estados (SP, MG, RS, PE, CE, entre outros).
  Um único conector CKAN parametrizado resolve dezenas de portais.
- **Querido Diário** cobre o que os portais não cobrem: 5.000+ municípios em
  full-text.
- **TCEs** trazem licitação e contrato municipal onde o PNCP ainda está incompleto
  — a adesão municipal ao PNCP não é uniforme.

---

## 26. Bibliotecas cliente — **nova**

Não são fontes, mas cortam semanas de parsing.

| Pacote | Cobre |
|---|---|
| `DadosAbertosBrasil` (Python) | IBGE, IPEA, BCB, Câmara, Senado |
| `basedosdados` (Python/R) | Datasets já tratados no BigQuery |
| `sidrapy` / `ipeadatapy` | SIDRA e Ipeadata em DataFrame |
| `python-cnpj` / loaders da RFB | Carga dos ~20 GB de CNPJ em Postgres/MySQL |
| `mcp-brasil` | ~70 fontes com ingestão bulk para DuckDB embarcado |

---

## Notas de engenharia

**Bulk sempre que existir.** As APIs REST governamentais brasileiras paginam mal,
têm rate limit não documentado e caem sob carga. Para carga histórica use os
arquivos: RFB CNPJ, TSE, INEP, RAIS/CAGED, DataSUS, repositório CSV do
Compras.gov.br. Reserve REST para o incremental diário e para o que só existe
como API (PNCP, Transparência, DataJud).

**Rate limit tem janela horária.** O Portal da Transparência libera 700 req/min
entre 00:00 e 06:00 e bem menos no horário comercial. Isso não é detalhe de
tuning: define que a ingestão pesada é job noturno, e que o agendamento precisa
respeitar America/Sao_Paulo, não UTC.

**Endereços mudam e quebram pipeline em silêncio.** A ANM migrou em fev/2026 e
manteve o endereço antigo respondendo até 30/06/2026 — quatro meses em que um
pipeline apontando para o lugar errado continua "funcionando". Guarde a URL de
origem como coluna na landing zone e alerte quando um domínio parar de aparecer.

**Qualidade é o problema real, não o volume.** Separador decimal ausente em
valores monetários, encoding Latin-1 misturado com UTF-8, CSVs com layout que
muda de ano para ano, campos-chave nulos, CNPJ ora com máscara ora sem. O
tratamento é o trabalho — e é o que diferencia o projeto de um tutorial.

**Chaves de junção que amarram tudo:** código IBGE de município (7 dígitos),
CNPJ (básico de 8 para a empresa, 14 para o estabelecimento), CNAE,
CATMAT/CATSER, código do órgão SIAFI/UASG **e código SIORG**, CEP. Modele essas
como dimensões conformadas desde o início — é o que permite cruzar compras com
empresas com território com população.

**Preço de referência é dimensão, não fato.** Para detecção de sobrepreço,
CMED (teto legal de medicamento), SIGTAP (valor SUS), BPS (preço praticado) e
Painel de Preços entram como faixas de referência versionadas por data de
vigência. Sem isso, "caro" vira comparação contra a própria média da base — que
é exatamente o que um cartel envenena.

**Captcha é uma decisão de arquitetura.** O SICAR não libera download
programático. Ou você aceita ingestão manual periódica, ou usa o espelho do
MapBiomas e assume a defasagem. Documente a escolha; ela muda a validade
temporal de qualquer análise fundiária.

**PII existe nessas bases.** TSE traz CPF e título de eleitor; Portal da
Transparência traz CPF parcial de servidores e beneficiários; DataSUS traz
microdados de saúde; SNCR e CadÚnico já vêm anonimizados mas com granularidade
reidentificável quando cruzados. Mascare na ingestão, não no consumo — e trate
cruzamento entre bases anonimizadas como risco de reidentificação, porque é.