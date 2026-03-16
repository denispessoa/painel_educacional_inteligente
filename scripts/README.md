# Scripts - Uso local

## Objetivo
Documentar os scripts do repositorio e a relacao deles com a arquitetura oficial do projeto.

## Baseline oficial
- `README.md`
- `SYSTEM_CONTEXT.md`
- `docs/EDUCATIONAL_DATA_ARCHITECTURE.md`
- `docs/MIGRATION_PLAN_EDUCATIONAL_ARCHITECTURE.md`

## Scripts principais
### `setup.sh`
Sobe a infraestrutura basica via Docker Compose.

Uso no PowerShell:
```powershell
docker compose up -d postgres api
```

### `provision_metabase_db.ps1`
Cria ou atualiza o banco de metadata do Metabase.

```powershell
.\scripts\provision_metabase_db.ps1
```

### `smoke_api.ps1`
Executa validacao rapida da API atual.

```powershell
.\scripts\smoke_api.ps1
```

### `backup_postgres.ps1` e `restore_postgres.ps1`
Backup e restore do banco `educacao`.

### `backup_metabase_db.ps1` e `restore_metabase_db.ps1`
Backup e restore do metadata DB do Metabase.

### `git_save.ps1`
Automatiza `git add`, `git commit` e `git push`.

## Scripts de BI
### `scripts/powerbi/`
Conectores legados para `/bi/v1/*`.

### `scripts/metabase/`
SQLs de apoio ao dashboard atual do Metabase.

## Regra de evolucao
Quando a camada oficial `avaliacoes -> fato_aprendizagem -> vw_desempenho_aprendizagem` entrar, revisar os scripts em 3 frentes:
1. infraestrutura tecnica
2. camada analitica
3. referencias pedagogicas
