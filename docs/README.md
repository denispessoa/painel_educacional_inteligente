# Docs - Indice tecnico

## Baselines oficiais
- `../README.md`
  - visao geral oficial do MVP e da arquitetura-alvo
- `../SYSTEM_CONTEXT.md`
  - contexto consolidado do sistema, hierarquia, ciclos e fontes de avaliacao
- `EDUCATIONAL_DATA_ARCHITECTURE.md`
  - arquitetura de dados educacionais e camada analitica de referencia
- `MIGRATION_PLAN_EDUCATIONAL_ARCHITECTURE.md`
  - plano oficial de migracao aditiva para `avaliacoes`, `ciclo_avaliativo`, `fato_aprendizagem` e `vw_desempenho_aprendizagem`
- `architecture_decisions/`
  - ADRs oficiais da fase atual (`ADR_007` a `ADR_011`)

## Estado atual do MVP
- CRUD operacional de `municipios`, `escolas` e `turmas`
- `indicadores_trimestrais` segue como camada operacional atual
- analytics atuais disponiveis via `/analytics/ima` e demais contratos entregues do MVP
- BI em transicao de Power BI para Metabase OSS
- arquitetura `Avaliacao -> fato_aprendizagem -> vw_desempenho_aprendizagem` definida como baseline oficial de evolucao, ainda em consolidacao tecnica

## Operacao e BI
- `OPERATIONS.md`
- `METABASE_SETUP.md`
- `METABASE_OPERATION.md`
- `METABASE_VALIDATION_CHECKLIST.md`
- `POWERBI_DESKTOP_CONNECTIONS.md`

## Contratos e planejamento
- `PHASE4_API_CONTRACT.md`
- `12_ROADMAP_POS_MVP.md`
- `13_PLANO_IMPLANTACAO_POS_MVP.md`
- `GITHUB_SETUP.md`

## Arquitetura e referencia pedagogica
- `CONVERGENCIA_AVALIACOES_BNCC_REDE.md`
- `IMA_REFERENCE_BASE.md`
- `PROJECT_ESSENCE_FOR_AI.md`
- `references/`
- `references/redes/`

## Checkpoints e contexto complementar
- `11_MINI_ROADMAP_30_DAYS.md`
- `ARCHITECTURE_UPDATE_BI.md`
- `STATUS_COMPONENTES_2026-03-16.md`
- `INCIDENT_RUNBOOK.md`

## Documentacao complementar fora desta pasta
- `../backend/README.md`
- `../backend/app/README.md`
- `../backend/tests/README.md`
- `../database/README.md`
- `../scripts/README.md`
