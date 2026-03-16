# Runbook Operacional (MVP)

## Escopo
Procedimentos tecnicos para operar o ambiente local do projeto ate a Fase 5.

## Checklist de pre-requisitos
- Docker Desktop em execucao
- Python instalado e acessivel no terminal
- Porta `5433` livre para Postgres local do projeto
- Porta `3000` livre para Metabase local
- Dependencias do backend instaladas em `backend/venv`

## Subida padrao do ambiente

### 1. Banco
Na raiz do repositorio:
```powershell
docker compose up -d postgres api
```

Validar container:
```powershell
docker compose ps
```

Smoke test da API:
```powershell
.\scripts\smoke_api.ps1
```

### 1.1 Provisionar metadata do Metabase
```powershell
Copy-Item .env.example .env
.\scripts\provision_metabase_db.ps1
```

### 1.2 Garantir `vw_ima`
```powershell
Get-Content .\database\views\ima_view.sql | docker compose exec -T postgres psql -U postgres -d educacao
```

### 1.3 Subir Metabase
```powershell
docker compose up -d metabase
```

Acesso local:
- API: `http://127.0.0.1:8000`
- Metabase: `http://127.0.0.1:3000`

### 2. API
Na pasta `backend`:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### 3. Health check
```powershell
curl http://127.0.0.1:8000/health
```
Esperado:
```json
{"status":"ok"}
```

Health de dependencias:
```powershell
curl http://127.0.0.1:8000/health/dependencies
```
Esperado:
```json
{"status":"ok","dependencies":{"database":"ok"}}
```

Metricas basicas:
```powershell
curl http://127.0.0.1:8000/metrics
```

## Rotina de testes
Na pasta `backend`:
```powershell
python -m pytest -q
```

## Validacao de endpoints BI (Fase 4)
Com a API em execucao:

```powershell
curl "http://127.0.0.1:8000/bi/v1/hierarquia"
curl "http://127.0.0.1:8000/bi/v1/indicadores-trimestrais?ano=2026&trimestre=1"
curl "http://127.0.0.1:8000/bi/v1/ima?group_by=municipio&ano=2026&trimestre=1"
```

Esperado:
- respostas `200`
- sem dados individuais de alunos
- no caso sem dados, listas vazias e resumo zerado para `/bi/v1/ima`

## Validacao de BI no Metabase (Fase 5.1)
- Seguir checklist em `docs/METABASE_VALIDATION_CHECKLIST.md`.
- Comparar indicadores com SQL no Postgres antes de cutover.

## Operacao de logs
Logs do Postgres:
```powershell
docker compose logs -f postgres
```

Logs do Metabase:
```powershell
docker compose logs -f metabase
```

Logs da API:
- em modo container:
```powershell
docker compose logs -f api
```
- em modo local:
  - observar output do processo `uvicorn` (eventos JSON de startup/request/shutdown)

## Reinicio rapido
Reiniciar somente banco:
```powershell
docker compose restart postgres
```

Reiniciar Metabase:
```powershell
docker compose restart metabase
```

Reiniciar API:
```powershell
docker compose restart api
```

## Reset completo de ambiente
Atencao: remove dados locais do banco.

```powershell
docker compose down -v
docker compose up -d postgres
Get-Content .\database\views\ima_view.sql | docker compose exec -T postgres psql -U postgres -d educacao
.\scripts\provision_metabase_db.ps1
docker compose up -d api metabase
```

## Backup e restore (Fase 5)
Gerar backup SQL:
```powershell
.\scripts\backup_postgres.ps1
```

Restaurar backup SQL:
```powershell
.\scripts\restore_postgres.ps1 -InputFile .\export\educacao_backup_YYYYMMDD_HHMMSS.sql
```

Backup do metadata DB do Metabase:
```powershell
.\scripts\backup_metabase_db.ps1
```

Restore do metadata DB do Metabase:
```powershell
.\scripts\restore_metabase_db.ps1 -InputFile .\export\metabase_backup_YYYYMMDD_HHMMSS.sql
```

## Troubleshooting rapido

### Docker daemon indisponivel
1. Abrir Docker Desktop.
2. Aguardar engine iniciar.
3. Reexecutar `docker compose up -d postgres api`.

### Erro ao ativar venv no PowerShell
Executar uma vez:
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### `uvicorn` ou `pytest` nao reconhecidos
Executar com modulo Python:
```powershell
python -m uvicorn app.main:app --reload
python -m pytest -q
```

### Erro de conexao com banco
Verificar:
1. `docker compose ps` com container `postgres` em estado `running`.
2. `DATABASE_URL` apontando para `localhost:5433`.
3. Se estiver usando a stack containerizada, validar `docker compose logs -f api`.

## Checklist de gate para inicio da Fase 4
- Documentacao tecnica critica criada e atualizada:
  - `README.md` (raiz)
  - `backend/README.md`
  - `backend/app/README.md`
  - `backend/tests/README.md`
  - `database/README.md`
  - `docs/PHASE4_API_CONTRACT.md`
- Contrato da Fase 4 definido sem decisoes abertas.

## Status atual
- Fase 4 implementada no backend com endpoints `/bi/v1/*`.
- Fase 5 iniciada com baseline operacional:
  - CI de backend
  - observabilidade minima (`/metrics`, `/health/dependencies`, logs JSON)
  - scripts de backup/restore
  - runbook de incidentes (`docs/INCIDENT_RUNBOOK.md`)
- Fase 5.1 em execucao:
  - Metabase OSS local em paralelo ao Power BI
  - metadata DB dedicado (`metabase`) no PostgreSQL
