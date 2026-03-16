# Database - Operacao e bootstrap

## Objetivo
Documentar como o banco PostgreSQL do MVP e inicializado e mantido localmente.

## Estrutura
- `sql/schema.sql`
  - DDL principal do modelo atual
- `sql/migrate_component_metrics.sql`
  - migracao incremental para bases locais que ainda estavam no contrato antigo
- `seeds/seed.sql`
  - carga demo idempotente com `1o-9o ano`, `2025-2026`, `CNCA` e `MEC Anos Finais BNCC`
- `views/ima_view.sql`
  - view legada `vw_ima`
- `views/desempenho_componentes_view.sql`
  - view canonica `vw_desempenho_componentes`
- `sql/provision_metabase_metadata.sql`
  - script idempotente para criar role/database de metadata do Metabase

## Ordem de bootstrap com Docker Compose
No `docker-compose.yml`, o Postgres monta:
1. `database/sql/schema.sql` como `01-schema.sql`
2. `database/seeds/seed.sql` como `02-seed.sql`

Para bases novas:
```powershell
docker compose up -d postgres
Get-Content .\database\views\ima_view.sql | docker compose exec -T postgres psql -U postgres -d educacao
Get-Content .\database\views\desempenho_componentes_view.sql | docker compose exec -T postgres psql -U postgres -d educacao
```

## Migracao de bases ja existentes
Se o volume do banco ja existia antes do modelo por componente:
```powershell
Get-Content .\database\sql\migrate_component_metrics.sql | docker compose exec -T postgres psql -U postgres -d educacao
Get-Content .\database\views\ima_view.sql | docker compose exec -T postgres psql -U postgres -d educacao
Get-Content .\database\views\desempenho_componentes_view.sql | docker compose exec -T postgres psql -U postgres -d educacao
Get-Content .\database\seeds\seed.sql | docker compose exec -T postgres psql -U postgres -d educacao
```

## Regras de integridade relevantes
- FK restritivas em toda a hierarquia
- `ano_escolar` entre `1` e `9`
- `fonte_avaliacao`:
  - `cnca` apenas para `1o-5o`
  - `mec_anos_finais_bncc` apenas para `6o-9o`
- campos canonicos:
  - `atingiu_esperado_leitura`
  - `atingiu_esperado_escrita`
  - `atingiu_esperado_matematica`
- campos legados mantidos temporariamente:
  - `alfabetizados_leitura`
  - `alfabetizados_escrita`
- unicidade:
  - `turma_id + ano + trimestre + ano_escolar + fonte_avaliacao`

## Validacao rapida no banco
```powershell
docker compose exec -T postgres psql -U postgres -d educacao -c "select count(*) from vw_desempenho_componentes;"
docker compose exec -T postgres psql -U postgres -d educacao -c "select fonte_avaliacao, min(ano_escolar), max(ano_escolar), count(*) from vw_desempenho_componentes group by fonte_avaliacao order by fonte_avaliacao;"
```

## Estado do dataset demo
- 3 municipios
- 3 escolas
- 9 turmas (`1o` ao `9o` ano)
- 72 registros trimestrais
- `CNCA`: 40 linhas (`1o-5o`)
- `MEC Anos Finais BNCC`: 32 linhas (`6o-9o`)
