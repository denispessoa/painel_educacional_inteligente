# Backend API (Fase 1-5)

API FastAPI do MVP da plataforma educacional.

Hierarquia de dados:
`Municipio -> Escola -> Turma -> IndicadorTrimestral`

## Requisitos
- Docker Desktop ativo
- Python 3.11+ (recomendado)
- PowerShell (Windows)

## Subir ambiente local

Modo containerizado na raiz do repositorio:

```powershell
docker compose up -d postgres api
```

Esse comando sobe:
- `postgres` na porta `5433`
- `api` na porta `8000`

Smoke test rapido da stack containerizada:
```powershell
.\scripts\smoke_api.ps1
```

Para a camada BI:
```powershell
Copy-Item .env.example .env
.\scripts\provision_metabase_db.ps1
docker compose up -d metabase
```

Modo desenvolvimento local na pasta `backend`:

```powershell
docker compose up -d postgres
docker compose stop api
```

Depois:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API:
- Swagger: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/health`

Observacao:
- para desenvolvimento diario, o fluxo recomendado continua sendo `postgres` via Docker e `uvicorn --reload` local;
- a API containerizada existe para smoke test, reproducao do ambiente e base de deploy.

## Variaveis de ambiente
- `DATABASE_URL`
  - default: `postgresql+psycopg://postgres:postgres@localhost:5433/educacao`
  - override (PowerShell):
```powershell
$env:DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5433/educacao"
```

## Matriz de endpoints (Fase 1-5)

### Health
| Metodo | Rota | Descricao |
| --- | --- | --- |
| GET | `/health` | health check da API |
| GET | `/health/dependencies` | health check de dependencias (banco) |
| GET | `/metrics` | metricas basicas de requests da API |

### Municipios
| Metodo | Rota | Filtros | Status principais |
| --- | --- | --- | --- |
| POST | `/municipios` | - | 201, 422 |
| GET | `/municipios` | `nome`, `estado` | 200, 422 |
| GET | `/municipios/{municipio_id}` | - | 200, 404 |
| PUT | `/municipios/{municipio_id}` | - | 200, 404, 422 |
| DELETE | `/municipios/{municipio_id}` | - | 204, 404, 409 |

### Escolas
| Metodo | Rota | Filtros | Status principais |
| --- | --- | --- | --- |
| POST | `/escolas` | - | 201, 409, 422 |
| GET | `/escolas` | `municipio_id`, `nome` | 200 |
| GET | `/escolas/{escola_id}` | - | 200, 404 |
| PUT | `/escolas/{escola_id}` | - | 200, 404, 409, 422 |
| DELETE | `/escolas/{escola_id}` | - | 204, 404, 409 |

### Turmas
| Metodo | Rota | Filtros | Status principais |
| --- | --- | --- | --- |
| POST | `/turmas` | - | 201, 409, 422 |
| GET | `/turmas` | `escola_id`, `nome` | 200 |
| GET | `/turmas/{turma_id}` | - | 200, 404 |
| PUT | `/turmas/{turma_id}` | - | 200, 404, 409, 422 |
| DELETE | `/turmas/{turma_id}` | - | 204, 404 |

### Indicadores trimestrais
| Metodo | Rota | Filtros | Status principais |
| --- | --- | --- | --- |
| POST | `/indicadores-trimestrais` | - | 201, 409, 422 |
| GET | `/indicadores-trimestrais` | `turma_id`, `ano`, `trimestre` | 200, 422 |
| GET | `/indicadores-trimestrais/{indicador_id}` | - | 200, 404 |
| PUT | `/indicadores-trimestrais/{indicador_id}` | - | 200, 404, 409, 422 |
| DELETE | `/indicadores-trimestrais/{indicador_id}` | - | 204, 404 |

### Analytics IMA (Fase 3)
| Metodo | Rota | Filtros | Status principais |
| --- | --- | --- | --- |
| GET | `/analytics/ima` | `group_by`, `ano`, `trimestre`, `municipio_id`, `escola_id`, `turma_id` | 200, 422 |

### Power BI v1 (Fase 4)
| Metodo | Rota | Filtros | Status principais |
| --- | --- | --- | --- |
| GET | `/bi/v1/hierarquia` | `municipio_id`, `escola_id`, `turma_id`, `estado` | 200, 422 |
| GET | `/bi/v1/indicadores-trimestrais` | `municipio_id`, `escola_id`, `turma_id`, `ano`, `trimestre` | 200, 422 |
| GET | `/bi/v1/ima` | `group_by`, `ano`, `trimestre`, `municipio_id`, `escola_id`, `turma_id` | 200, 422 |

## Observabilidade minima (Fase 5)
- Logs estruturados JSON para startup/shutdown e requests HTTP.
- Middleware com:
  - `x-request-id` em responses
  - tempo de resposta por request
  - contagem por faixa de status (`2xx`, `4xx`, `5xx`)
- Endpoint `/metrics` com snapshot das metricas basicas da API.
- Endpoint `/health/dependencies` para validar conectividade do banco.

## Contrato de erro

### `422 Unprocessable Entity`
- Erro de validacao de schema ou query.
- Exemplo:
```json
{
  "detail": [
    {
      "type": "less_than_equal",
      "loc": ["query", "trimestre"],
      "msg": "Input should be less than or equal to 4",
      "input": 5,
      "ctx": {"le": 4}
    }
  ]
}
```

### `404 Not Found`
- Recurso nao encontrado.
- Exemplo:
```json
{
  "detail": "municipio nao encontrado"
}
```

### `409 Conflict`
- Violacao de integridade referencial ou duplicidade logica.
- Exemplos de `detail` possiveis:
  - `municipio possui escolas vinculadas`
  - `escola possui turmas vinculadas`
  - `municipio informado nao existe`
  - `escola informada nao existe`
  - `turma informada nao existe`
  - `ja existe indicador para esta turma, ano e trimestre`

Observacao para Fase 4:
- Endpoints `/bi/v1/*` sao read-only e nao usam `404`/`409` como fluxo esperado.

## Exemplos de request/response

### Criar municipio
Request:
```http
POST /municipios
Content-Type: application/json
```
```json
{
  "nome": "Mendes",
  "estado": "rj"
}
```

Response `201`:
```json
{
  "id": "1b4e3d48-c2aa-4efa-b50a-95f4f91be1d0",
  "nome": "Mendes",
  "estado": "RJ"
}
```

### Criar indicador trimestral
Request:
```http
POST /indicadores-trimestrais
Content-Type: application/json
```
```json
{
  "turma_id": "b99de1a5-8e2e-4eb1-951f-8b5b57ffb0f2",
  "ano": 2026,
  "trimestre": 1,
  "total_alunos": 30,
  "alfabetizados_leitura": 21,
  "alfabetizados_escrita": 18
}
```

Response `201`:
```json
{
  "id": "f2c59f0a-6e2b-420f-8e38-27ef7194db8e",
  "turma_id": "b99de1a5-8e2e-4eb1-951f-8b5b57ffb0f2",
  "ano": 2026,
  "trimestre": 1,
  "total_alunos": 30,
  "alfabetizados_leitura": 21,
  "alfabetizados_escrita": 18,
  "percentual_leitura": 70.0,
  "percentual_escrita": 60.0
}
```

### Consultar analytics IMA
Request:
```http
GET /analytics/ima?group_by=municipio&ano=2026&trimestre=1
```

Response `200`:
```json
{
  "filtros": {
    "group_by": "municipio",
    "ano": 2026,
    "trimestre": 1,
    "municipio_id": null,
    "escola_id": null,
    "turma_id": null
  },
  "resumo": {
    "total_registros": 3,
    "total_alunos": 60,
    "percentual_leitura_medio": 61.67,
    "percentual_escrita_medio": 58.33,
    "ima_medio": 60.0
  },
  "itens": [
    {
      "nivel": "municipio",
      "id": "1b4e3d48-c2aa-4efa-b50a-95f4f91be1d0",
      "nome": "Mendes (RJ)",
      "total_registros": 3,
      "total_alunos": 60,
      "percentual_leitura_medio": 61.67,
      "percentual_escrita_medio": 58.33,
      "ima_medio": 60.0
    }
  ]
}
```

### Consultar BI v1 indicadores trimestrais
Request:
```http
GET /bi/v1/indicadores-trimestrais?ano=2026&trimestre=1
```

Response `200`:
```json
[
  {
    "indicador_id": "f2c59f0a-6e2b-420f-8e38-27ef7194db8e",
    "ano": 2026,
    "trimestre": 1,
    "turma_id": "b99de1a5-8e2e-4eb1-951f-8b5b57ffb0f2",
    "turma_nome": "Turma A",
    "escola_id": "f5d61d2f-016c-4658-a2ca-70f8a9e54447",
    "escola_nome": "Escola A",
    "municipio_id": "1b4e3d48-c2aa-4efa-b50a-95f4f91be1d0",
    "municipio_nome": "Mendes",
    "municipio_estado": "RJ",
    "total_alunos": 30,
    "alfabetizados_leitura": 21,
    "alfabetizados_escrita": 18,
    "percentual_leitura": 70.0,
    "percentual_escrita": 60.0,
    "ima": 65.0
  }
]
```

## Testes

Na pasta `backend`:

```powershell
python -m pytest -q
```

Pipeline CI:
- arquivo: `.github/workflows/backend-ci.yml`
- executa `pip check` + `pytest` + `docker build` automaticamente em `push`/`pull_request`.

Arquivos de teste por dominio:
- `tests/test_health.py`
- `tests/test_municipios.py`
- `tests/test_escolas.py`
- `tests/test_turmas.py`
- `tests/test_indicadores_trimestrais.py`
- `tests/test_analytics_ima.py`
- `tests/test_bi_v1.py`

## Troubleshooting (Windows)

### Docker nao sobe
Sintoma:
- erro de conexao com daemon Docker.

Acao:
1. Abrir Docker Desktop.
2. Aguardar status "Engine running".
3. Rodar novamente `docker compose up -d postgres api`.
4. Validar com `.\scripts\smoke_api.ps1`.

### Erro ao ativar `venv`
Sintoma:
- script bloqueado por politica de execucao.

Acao (PowerShell como admin):
```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
Depois:
```powershell
.\venv\Scripts\Activate.ps1
```

### `uvicorn app.main:app --reload` falha
Sintomas comuns:
- `ModuleNotFoundError: No module named 'app'`
- comando nao encontrado.

Acao:
1. Entrar em `backend`.
2. Ativar `venv`.
3. Garantir dependencias instaladas.
4. Rodar:
```powershell
python -m uvicorn app.main:app --reload
```

### `pytest` nao reconhecido
Acao:
```powershell
python -m pytest -q
```
