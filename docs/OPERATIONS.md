# Runbook Operacional (MVP)

## Escopo
Procedimentos tecnicos para operar o ambiente local do projeto ate a Fase 5, incluindo o modelo atual de desempenho por componente.

## Checklist de pre-requisitos
- Docker Desktop em execucao
- Python instalado e acessivel no terminal
- Porta `5433` livre para Postgres local do projeto
- Porta `3000` livre para Metabase local
- Dependencias do backend instaladas em `backend/venv`

## Subida padrao do ambiente

### 1. Banco e API
Na raiz do repositorio:
```powershell
docker compose up -d postgres api
```

Validar containers:
```powershell
docker compose ps
```

Smoke test da API:
```powershell
.\scripts\smoke_api.ps1
```

### 1.1 Migrar banco local para o modelo de componentes
Se o volume do Postgres ja existia antes desta revisao:
```powershell
Get-Content .\database\sql\migrate_component_metrics.sql | docker compose exec -T postgres psql -U postgres -d educacao
Get-Content .\database\views\ima_view.sql | docker compose exec -T postgres psql -U postgres -d educacao
Get-Content .\database\views\desempenho_componentes_view.sql | docker compose exec -T postgres psql -U postgres -d educacao
Get-Content .\database\seeds\seed.sql | docker compose exec -T postgres psql -U postgres -d educacao
```

### 1.2 Provisionar metadata do Metabase
```powershell
Copy-Item .env.example .env
.\scripts\provision_metabase_db.ps1
```

### 1.3 Subir Metabase
```powershell
docker compose up -d metabase
```

Acesso local:
- API: `http://127.0.0.1:8000`
- Metabase: `http://127.0.0.1:3000`

## Rotina de desenvolvimento local
Na pasta `backend`:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

## Health checks
```powershell
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/health/dependencies
curl http://127.0.0.1:8000/metrics
```

## Rotina de testes
Na pasta `backend`:
```powershell
python -m pytest -q
```

## Validacao de endpoints principais
Com a API em execucao:

```powershell
curl "http://127.0.0.1:8000/analytics/desempenho?group_by=municipio&ano=2026&trimestre=4"
curl "http://127.0.0.1:8000/bi/v1/indicadores-componentes?ano=2026&trimestre=4"
curl "http://127.0.0.1:8000/bi/v1/desempenho?group_by=municipio&ano=2026&trimestre=4"
```

Legado temporario:
```powershell
curl "http://127.0.0.1:8000/analytics/ima?group_by=municipio&ano=2026&trimestre=4"
curl "http://127.0.0.1:8000/bi/v1/ima?group_by=municipio&ano=2026&trimestre=4"
```

## Validacao rapida no banco
```powershell
docker compose exec -T postgres psql -U postgres -d educacao -c "select count(*) from vw_desempenho_componentes;"
docker compose exec -T postgres psql -U postgres -d educacao -c "select fonte_avaliacao, min(ano_escolar), max(ano_escolar), count(*) from vw_desempenho_componentes group by fonte_avaliacao order by fonte_avaliacao;"
```

## Validacao do Metabase
- view principal nova: `vw_desempenho_componentes`
- view legada: `vw_ima`
- scripts de apoio: `scripts/metabase/`
- checklist de paridade: `docs/METABASE_VALIDATION_CHECKLIST.md`

## Reset completo de ambiente
Atencao: remove dados locais do banco.

```powershell
docker compose down -v
docker compose up -d postgres
Get-Content .\database\views\ima_view.sql | docker compose exec -T postgres psql -U postgres -d educacao
Get-Content .\database\views\desempenho_componentes_view.sql | docker compose exec -T postgres psql -U postgres -d educacao
.\scripts\provision_metabase_db.ps1
docker compose up -d api metabase
```

## Troubleshooting rapido

### Banco com contrato antigo
Reaplicar migracao e seed:
```powershell
Get-Content .\database\sql\migrate_component_metrics.sql | docker compose exec -T postgres psql -U postgres -d educacao
Get-Content .\database\seeds\seed.sql | docker compose exec -T postgres psql -U postgres -d educacao
```

### `uvicorn` ou `pytest` nao reconhecidos
```powershell
python -m uvicorn app.main:app --reload
python -m pytest -q
```

### Docker daemon indisponivel
1. Abrir Docker Desktop.
2. Aguardar engine iniciar.
3. Reexecutar `docker compose up -d postgres api`.

## Status atual
- `analytics/desempenho` e `bi/v1/desempenho` ativos
- `vw_desempenho_componentes` criada para a camada BI principal
- `IMA` mantido apenas como legado temporario
- seed demo cobre `1o-9o ano` com:
  - `CNCA` para `1o-5o`
  - `MEC Anos Finais BNCC` para `6o-9o`
