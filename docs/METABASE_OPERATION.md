# Metabase Operacao (Fase 5.1)

Runbook de uso diario do Metabase local no projeto.

## Escopo
- Operacao em paralelo ao Power BI.
- Metabase como camada BI sem custo de licenca.
- Sem alteracao de contratos da API.

## Comandos operacionais

### Subir stack BI local
```powershell
docker compose up -d postgres
.\scripts\provision_metabase_db.ps1
Get-Content .\database\views\ima_view.sql | docker compose exec -T postgres psql -U postgres -d educacao
docker compose up -d metabase
```

### Ver status
```powershell
docker compose ps
```

### Ver logs do Metabase
```powershell
docker compose logs -f metabase
```

### Reiniciar Metabase
```powershell
docker compose restart metabase
```

### Parar Metabase (mantendo Postgres)
```powershell
docker compose stop metabase
```

## Backup e restore

### Banco de negocio (`educacao`)
Backup:
```powershell
.\scripts\backup_postgres.ps1
```

Restore:
```powershell
.\scripts\restore_postgres.ps1 -InputFile .\export\educacao_backup_YYYYMMDD_HHMMSS.sql
```

### Metadata do Metabase (`metabase`)
Backup:
```powershell
.\scripts\backup_metabase_db.ps1
```

Restore:
```powershell
.\scripts\restore_metabase_db.ps1 -InputFile .\export\metabase_backup_YYYYMMDD_HHMMSS.sql
```

## Checklist de saude diaria
1. `docker compose ps` com `postgres` e `metabase` em `running`.
2. Abrir `http://127.0.0.1:3000`.
3. Dashboard MVP carregando sem erro.
4. Consulta de KPI retornando valores.

## Plano de rollback (durante transicao)
Se o Metabase falhar e bloquear operacao:
1. Manter API e banco como estao (sem alteracao de schema).
2. Retornar uso operacional ao Power BI (docs legadas).
3. Corrigir Metabase sem pressao de indisponibilidade do BI.

## Limites desta fase
- Sem deploy remoto do Metabase.
- Sem SSO/autenticacao corporativa.
- Sem desativar Power BI antes de checklist de paridade completo.
