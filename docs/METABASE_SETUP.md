# Metabase Setup Local (Fase 5.1)

Guia para subir Metabase OSS localmente em paralelo ao Power BI.

## Objetivo
- Operar BI sem custo de licenca.
- Manter compatibilidade com a API e banco atuais.
- Validar dashboards no Metabase antes de cutover.

## Pre-requisitos
- Docker Desktop ativo.
- Projeto com `postgres` funcional em `docker compose`.
- PowerShell (Windows).

## 1) Configurar variaveis do Metabase
Copie o arquivo de exemplo e ajuste os valores:

```powershell
Copy-Item .env.example .env
```

Campos esperados no `.env`:
- `METABASE_DB_NAME` (default: `metabase`)
- `METABASE_DB_USER` (default: `metabase`)
- `METABASE_DB_PASS` (trocar em ambientes reais)
- `METABASE_ENCRYPTION_SECRET_KEY` (trocar em ambientes reais)

## 2) Subir Postgres e provisionar metadata do Metabase
```powershell
docker compose up -d postgres
.\scripts\provision_metabase_db.ps1
```

## 3) Garantir view analitica para dashboards
```powershell
Get-Content .\database\views\ima_view.sql | docker compose exec -T postgres psql -U postgres -d educacao
```

## 4) Subir Metabase
```powershell
docker compose up -d metabase
docker compose ps
```

Esperado:
- `postgres` e `metabase` em `running`.
- Metabase acessivel em `http://127.0.0.1:3000`.

## 5) Onboarding inicial no navegador
1. Acessar `http://127.0.0.1:3000`.
2. Criar usuario admin local.
3. Em "Add your data", configurar PostgreSQL com:
   - Host: `postgres`
   - Port: `5432`
   - Database: `educacao`
   - Username: `postgres`
   - Password: `postgres`
4. Habilitar sync/scan (padrao recomendado).

## 6) Modelagem minima recomendada
Base principal:
- `vw_ima`

Dimensoes de apoio:
- `municipios`
- `escolas`
- `turmas`
- `indicadores_trimestrais`

Padrao de filtros no Metabase:
- `ano`
- `trimestre`
- `municipio_nome`

## 7) Dashboard MVP equivalente
Colecao:
- `MVP Educacao`

Dashboard:
- `MVP - Alfabetizacao e IMA`

Cards/KPIs:
- `Qtd Linhas` -> `COUNT(*)` em `vw_ima`
- `Total Alunos` -> `SUM(total_alunos)`
- `Media Leitura` -> `AVG(percentual_leitura)`
- `Media Escrita` -> `AVG(percentual_escrita)`
- `IMA Medio` -> `AVG(ima)`

Visuais minimos:
- Cards KPI
- Serie temporal por trimestre usando a coluna `periodo` da query
- Comparativo por municipio

## 8) Validacao inicial rapida
1. Metabase abre sem erro.
2. Banco `educacao` conectado.
3. `vw_ima` visivel no Data Model.
4. Dashboard MVP criado e com dados.

## Troubleshooting rapido

### Metabase nao sobe
```powershell
docker compose logs -f metabase
```

Se erro de conexao no metadata DB:
1. Reexecutar `.\scripts\provision_metabase_db.ps1`.
2. Reiniciar Metabase:
```powershell
docker compose restart metabase
```

### Banco `educacao` nao aparece no Metabase
1. Verificar `postgres` em running:
```powershell
docker compose ps
```
2. Validar credenciais informadas no onboarding.
3. Forcar sync no admin do Metabase.
