# Scripts - Uso local

## `setup.sh`
Script simples para subir dependencias de infraestrutura via Docker Compose.

Conteudo atual:
```bash
docker compose up -d postgres
```

## Como usar
Em ambientes Unix/Linux:
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

No Windows/PowerShell, preferir comando direto:
```powershell
docker compose up -d postgres
```

## Pre-requisitos
- Docker Desktop ativo
- Docker Compose disponivel no PATH

## Provisionamento Metabase (Fase 5.1)
### `provision_metabase_db.ps1`
Cria/atualiza role e database de metadata do Metabase no PostgreSQL local.

Uso padrao:
```powershell
.\scripts\provision_metabase_db.ps1
```

Com parametros customizados:
```powershell
.\scripts\provision_metabase_db.ps1 -MetabaseDbName metabase -MetabaseDbUser metabase -MetabaseDbPass "troque_esta_senha"
```

## Backup e restore (Fase 5)
### `git_save.ps1`
Automatiza `git add .`, `git commit` e `git push`.

Uso padrao:
```powershell
.\scripts\git_save.ps1 -Message "docs: atualiza guia do metabase"
```

Primeira conexao com GitHub no mesmo comando:
```powershell
.\scripts\git_save.ps1 -Message "chore: primeiro push" -RemoteUrl https://github.com/SEU-USUARIO/educacao-inteligente.git
```

Validar sem executar:
```powershell
.\scripts\git_save.ps1 -Message "teste" -DryRun
```

Criar commit sem push:
```powershell
.\scripts\git_save.ps1 -Message "wip: ajustes locais" -SkipPush
```

### `backup_postgres.ps1`
Gera backup SQL do banco `educacao` no container `postgres`.

Uso padrao:
```powershell
.\scripts\backup_postgres.ps1
```

Com caminho customizado:
```powershell
.\scripts\backup_postgres.ps1 -OutputFile .\export\educacao_backup_manual.sql
```

### `restore_postgres.ps1`
Restaura um arquivo SQL no banco `educacao`.

Uso:
```powershell
.\scripts\restore_postgres.ps1 -InputFile .\export\educacao_backup_manual.sql
```

### `backup_metabase_db.ps1`
Gera backup SQL do metadata DB do Metabase.

Uso:
```powershell
.\scripts\backup_metabase_db.ps1
```

### `restore_metabase_db.ps1`
Restaura backup SQL no metadata DB do Metabase.

Uso:
```powershell
.\scripts\restore_metabase_db.ps1 -InputFile .\export\metabase_backup_YYYYMMDD_HHMMSS.sql
```

## Scripts Power BI
- Pasta: `scripts/powerbi/`
- Contem consultas `.pq` prontas para:
  - `/bi/v1/hierarquia`
  - `/bi/v1/indicadores-trimestrais`
  - `/bi/v1/ima`
- Guia de uso: `scripts/powerbi/README.md`
- Status: legado temporario durante migracao para Metabase.

## Scripts Metabase
- Pasta: `scripts/metabase/`
- Contem SQL base para o dashboard MVP:
  - `kpi_cards.sql`
  - `serie_trimestral.sql`
  - `comparativo_municipio.sql`
- Guia de uso: `scripts/metabase/README.md`
