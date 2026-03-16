# Backend API

## Baseline oficial
Arquitetura oficial do projeto:
`Municipio -> Escola -> Turma -> Avaliacao -> Indicadores de aprendizagem`

Pipeline analitico oficial:
`Avaliacoes da Rede -> fato_aprendizagem -> vw_desempenho_aprendizagem -> Metabase`

## Estado atual implementado
- CRUD de `municipios`, `escolas` e `turmas`
- `indicadores_trimestrais`
- analytics atuais do MVP
- endpoints `/bi/v1/*` entregues para a camada BI legada

## O que ainda nao esta fechado na API
- CRUD de `avaliacoes`
- contrato HTTP da camada `fato_aprendizagem`
- contrato HTTP final da camada `vw_desempenho_aprendizagem`

## Requisitos locais
- Docker Desktop ativo
- Python 3.11+
- PowerShell no Windows

## Subir ambiente containerizado
```powershell
docker compose up -d postgres api
.\scripts\smoke_api.ps1
```

## Desenvolvimento local
```powershell
docker compose up -d postgres
docker compose stop api
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

## Endpoints atuais
### Health
- `/health`
- `/health/dependencies`
- `/metrics`

### CRUD atual
- `/municipios`
- `/escolas`
- `/turmas`
- `/indicadores-trimestrais`

### Analytics atual
- `/analytics/ima`
- demais endpoints atualmente implementados no MVP devem ser lidos em conjunto com o codigo e os testes

### BI atual
- `/bi/v1/hierarquia`
- `/bi/v1/indicadores-trimestrais`
- `/bi/v1/ima`

## Contrato de erro atual do MVP
- `422` para validacao
- `404` para recurso nao encontrado
- `409` para conflito de integridade

## Regra de evolucao
Toda evolucao para `avaliacoes`, `ciclo_avaliativo`, `fato_aprendizagem` e `vw_desempenho_aprendizagem` deve atualizar em conjunto:
- modelos
- schemas
- routers
- testes
- `backend/README.md`
- `docs/MIGRATION_PLAN_EDUCATIONAL_ARCHITECTURE.md`
- ADRs correspondentes
