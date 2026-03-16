# Plataforma Municipal de Inteligencia Educacional (MVP)

Repositorio do MVP da plataforma municipal com foco em dados agregados de alfabetizacao.

## Objetivo
- Entregar API backend para operacao municipal.
- Manter hierarquia: `Municipio -> Escola -> Turma -> Indicadores`.
- Operar BI com custo reduzido em transicao Power BI -> Metabase OSS.

## Escopo atual
- Fase 1: CRUD de municipios, escolas e turmas.
- Fase 2: indicadores trimestrais de leitura e escrita.
- Fase 3: endpoint de analytics IMA.
- Fase 4: endpoints de leitura para Power BI (`/bi/v1/*`).
- Fase 5 (inicio): baseline operacional (CI backend, observabilidade minima e backup/restore).
- Fase 5.1: migracao de BI para Metabase OSS em paralelo ao Power BI.

## Restricoes do MVP
- Nao implementar RBAC completo nesta etapa.
- Nao coletar dados individuais de alunos.
- Seguir ordem definida em `CODEX_TASKS.md`.

## Stack
- FastAPI
- SQLAlchemy 2.0
- PostgreSQL
- Metabase OSS (camada BI principal em transicao)
- Power BI (legado temporario para rollback)

## Estrutura do repositorio
- `backend/`: API FastAPI, modelos, schemas, CRUD, routers e testes.
- `database/`: schema SQL, seeds e view de apoio para BI.
- `docs/`: documentos de arquitetura, operacao e contrato da Fase 4.
- `scripts/`: scripts de bootstrap local.

## Quickstart local (Windows PowerShell)
### Modo A - Stack containerizada
1. Subir API + banco:
```powershell
docker compose up -d postgres api
```
2. Validar a API containerizada:
```powershell
.\scripts\smoke_api.ps1
```
3. Subir Metabase local quando precisar da camada BI:
```powershell
Copy-Item .env.example .env
.\scripts\provision_metabase_db.ps1
docker compose up -d metabase
```

### Modo B - Desenvolvimento local com hot reload
1. Subir somente o banco:
```powershell
docker compose up -d postgres
```
2. Se o container `api` estiver rodando, parar antes:
```powershell
docker compose stop api
```
3. Configurar backend:
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
4. Subir API localmente:
```powershell
uvicorn app.main:app --reload
```
5. Executar testes:
```powershell
python -m pytest -q
```

## Variaveis de ambiente
- `DATABASE_URL`
  - Default: `postgresql+psycopg://postgres:postgres@localhost:5433/educacao`
  - Exemplo:
```powershell
$env:DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5433/educacao"
```

## Documentacao tecnica
- `docs/README.md` (indice)
- `docs/OPERATIONS.md` (runbook operacional)
- `docs/METABASE_SETUP.md` (setup local Metabase)
- `docs/METABASE_OPERATION.md` (operacao BI Metabase)
- `docs/METABASE_VALIDATION_CHECKLIST.md` (paridade Metabase x SQL)
- `docs/GITHUB_SETUP.md` (publicacao no GitHub e fluxo de versionamento)
- `docs/PHASE4_API_CONTRACT.md` (contrato fechado para endpoints BI da Fase 4)
- `docs/POWERBI_DESKTOP_CONNECTIONS.md` (legado temporario no Power BI Desktop)
- `docs/12_ROADMAP_POS_MVP.md` (fases 5-8)
- `docs/13_PLANO_IMPLANTACAO_POS_MVP.md` (implantacao das fases pos-MVP)
- `backend/README.md` (operacao da API + contrato HTTP Fase 1-3)
- `backend/app/README.md` (arquitetura interna)
- `backend/tests/README.md` (estrategia e execucao de testes)
- `database/README.md` (bootstrap e operacao do banco)
- `scripts/README.md` (uso de scripts)
