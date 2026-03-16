# Database - Operacao e bootstrap

## Objetivo
Documentar como o banco PostgreSQL do MVP e inicializado e mantido localmente.

## Estrutura
- `sql/schema.sql`
  - DDL principal (tabelas, constraints, indices)
  - inclui:
    - `municipios`
    - `escolas`
    - `turmas`
    - `indicadores_trimestrais`
- `seeds/seed.sql`
  - carga inicial minima de dados
- `views/ima_view.sql`
  - view `vw_ima` com dados denormalizados para consumo analitico/BI
- `sql/provision_metabase_metadata.sql`
  - script idempotente para criar role/database de metadata do Metabase

## Ordem de bootstrap com Docker Compose
No `docker-compose.yml`, o Postgres monta:
1. `database/sql/schema.sql` como `01-schema.sql`
2. `database/seeds/seed.sql` como `02-seed.sql`

Comandos:
```powershell
docker compose up -d postgres
```

## Aplicacao da view `vw_ima`
O arquivo de view nao esta montado automaticamente no entrypoint do container.
Aplicar manualmente quando necessario:

```powershell
Get-Content .\database\views\ima_view.sql | docker compose exec -T postgres psql -U postgres -d educacao
```

## Provisionamento do metadata DB do Metabase
Script operacional:
```powershell
.\scripts\provision_metabase_db.ps1
```

## Reset completo do banco local
Atencao: remove volume e todos os dados locais.

```powershell
docker compose down -v
docker compose up -d postgres
```

Depois do reset, reaplicar view:
```powershell
Get-Content .\database\views\ima_view.sql | docker compose exec -T postgres psql -U postgres -d educacao
```

## Validacao rapida no banco
Listar tabelas:
```powershell
docker compose exec postgres psql -U postgres -d educacao -c "\dt"
```

Contar municipios seed:
```powershell
docker compose exec postgres psql -U postgres -d educacao -c "select count(*) from municipios;"
```

## Regras de integridade relevantes
- FK restritivas:
  - `escolas.municipio_id -> municipios.id (RESTRICT)`
  - `turmas.escola_id -> escolas.id (RESTRICT)`
  - `indicadores_trimestrais.turma_id -> turmas.id (RESTRICT)`
- Unicidade de periodo:
  - `UNIQUE (turma_id, ano, trimestre)` em `indicadores_trimestrais`
- Checks:
  - faixas de `ano` e `trimestre`
  - totais e percentuais nao negativos
  - alfabetizados <= total
