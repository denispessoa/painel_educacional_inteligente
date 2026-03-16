# Backend API (Fase 1-5)

API FastAPI do MVP da plataforma educacional.

Hierarquia de dados:
`Municipio -> Escola -> Turma -> IndicadorTrimestral`

Estado semantico atual:
- `1o-5o ano`: base operacional `CNCA`
- `6o-9o ano`: base operacional `MEC Anos Finais BNCC`
- metrica principal: `percentual no esperado` por componente (`leitura`, `escrita`, `matematica`)
- `IMA` permanece disponivel apenas como legado temporario para compatibilidade

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

## Variaveis de ambiente
- `DATABASE_URL`
  - default: `postgresql+psycopg://postgres:postgres@localhost:5433/educacao`

## Matriz de endpoints

### Health
| Metodo | Rota | Descricao |
| --- | --- | --- |
| GET | `/health` | health check da API |
| GET | `/health/dependencies` | health check de dependencias |
| GET | `/metrics` | metricas basicas de requests |

### CRUD base
| Metodo | Rota | Filtros | Status principais |
| --- | --- | --- | --- |
| POST | `/municipios` | - | 201, 422 |
| GET | `/municipios` | `nome`, `estado` | 200, 422 |
| GET | `/municipios/{municipio_id}` | - | 200, 404 |
| PUT | `/municipios/{municipio_id}` | - | 200, 404, 422 |
| DELETE | `/municipios/{municipio_id}` | - | 204, 404, 409 |
| POST | `/escolas` | - | 201, 409, 422 |
| GET | `/escolas` | `municipio_id`, `nome` | 200 |
| GET | `/escolas/{escola_id}` | - | 200, 404 |
| PUT | `/escolas/{escola_id}` | - | 200, 404, 409, 422 |
| DELETE | `/escolas/{escola_id}` | - | 204, 404, 409 |
| POST | `/turmas` | - | 201, 409, 422 |
| GET | `/turmas` | `escola_id`, `nome` | 200 |
| GET | `/turmas/{turma_id}` | - | 200, 404 |
| PUT | `/turmas/{turma_id}` | - | 200, 404, 409, 422 |
| DELETE | `/turmas/{turma_id}` | - | 204, 404 |

### Indicadores trimestrais
| Metodo | Rota | Filtros | Status principais |
| --- | --- | --- | --- |
| POST | `/indicadores-trimestrais` | - | 201, 409, 422 |
| GET | `/indicadores-trimestrais` | `turma_id`, `ano`, `trimestre`, `ano_escolar`, `fonte_avaliacao` | 200, 422 |
| GET | `/indicadores-trimestrais/{indicador_id}` | - | 200, 404 |
| PUT | `/indicadores-trimestrais/{indicador_id}` | - | 200, 404, 409, 422 |
| DELETE | `/indicadores-trimestrais/{indicador_id}` | - | 204, 404 |

### Analytics
| Metodo | Rota | Filtros | Status principais |
| --- | --- | --- | --- |
| GET | `/analytics/desempenho` | `group_by`, `ano`, `trimestre`, `ano_escolar`, `fonte_avaliacao`, `municipio_id`, `escola_id`, `turma_id` | 200, 422 |
| GET | `/analytics/ima` | mesmos filtros | 200, 422 |

Observacao:
- `/analytics/desempenho` e o endpoint principal.
- `/analytics/ima` esta mantido por compatibilidade e deve ser tratado como legado.

### BI v1
| Metodo | Rota | Filtros | Status principais |
| --- | --- | --- | --- |
| GET | `/bi/v1/hierarquia` | `municipio_id`, `escola_id`, `turma_id`, `estado` | 200, 422 |
| GET | `/bi/v1/indicadores-componentes` | `municipio_id`, `escola_id`, `turma_id`, `ano`, `trimestre`, `ano_escolar`, `fonte_avaliacao` | 200, 422 |
| GET | `/bi/v1/desempenho` | `group_by`, `ano`, `trimestre`, `ano_escolar`, `fonte_avaliacao`, `municipio_id`, `escola_id`, `turma_id` | 200, 422 |
| GET | `/bi/v1/indicadores-trimestrais` | mesmos filtros | 200, 422 |
| GET | `/bi/v1/ima` | mesmos filtros agregados | 200, 422 |

Observacao:
- `/bi/v1/indicadores-componentes` e `/bi/v1/desempenho` sao os contratos recomendados.
- `/bi/v1/indicadores-trimestrais` e `/bi/v1/ima` permanecem como legados temporarios.

## Contrato semantico dos indicadores
- `ano_escolar`: inteiro entre `1` e `9`
- `fonte_avaliacao`:
  - `cnca` para `1o-5o`
  - `mec_anos_finais_bncc` para `6o-9o`
- `atingiu_esperado_leitura`
- `atingiu_esperado_escrita`
- `atingiu_esperado_matematica`
- `percentual_*`: calculado no backend
- criterio de atingimento:
  - `Proficiente + Avancado`

Campos legados ainda expostos por compatibilidade:
- `alfabetizados_leitura`
- `alfabetizados_escrita`

Esses dois campos hoje sao aliases de `atingiu_esperado_leitura` e `atingiu_esperado_escrita` e estao marcados como deprecated.

## Contrato de erro

### `422 Unprocessable Entity`
- erro de validacao estrutural ou regra de negocio
- exemplos:
  - `ano_escolar` fora de `1..9`
  - `fonte_avaliacao` incompativel com a etapa
  - `atingiu_esperado_matematica > total_alunos`

### `404 Not Found`
- recurso CRUD nao encontrado

### `409 Conflict`
- conflito de integridade referencial ou duplicidade logica
- exemplos:
  - `turma informada nao existe`
  - `ja existe indicador para esta turma, ano, trimestre, ano_escolar e fonte_avaliacao`

## Exemplos de request/response

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
  "ano_escolar": 4,
  "fonte_avaliacao": "cnca",
  "total_alunos": 30,
  "atingiu_esperado_leitura": 21,
  "atingiu_esperado_escrita": 18,
  "atingiu_esperado_matematica": 16
}
```

Response `201`:
```json
{
  "id": "f2c59f0a-6e2b-420f-8e38-27ef7194db8e",
  "turma_id": "b99de1a5-8e2e-4eb1-951f-8b5b57ffb0f2",
  "ano": 2026,
  "trimestre": 1,
  "ano_escolar": 4,
  "fonte_avaliacao": "cnca",
  "total_alunos": 30,
  "atingiu_esperado_leitura": 21,
  "atingiu_esperado_escrita": 18,
  "atingiu_esperado_matematica": 16,
  "alfabetizados_leitura": 21,
  "alfabetizados_escrita": 18,
  "percentual_leitura": 70.0,
  "percentual_escrita": 60.0,
  "percentual_matematica": 53.33
}
```

### Consultar analytics de desempenho
Request:
```http
GET /analytics/desempenho?group_by=municipio&ano=2026&trimestre=4
```

Response `200`:
```json
{
  "filtros": {
    "group_by": "municipio",
    "ano": 2026,
    "trimestre": 4,
    "ano_escolar": null,
    "fonte_avaliacao": null,
    "municipio_id": null,
    "escola_id": null,
    "turma_id": null
  },
  "resumo": {
    "total_registros": 9,
    "total_alunos": 198,
    "percentual_leitura_no_esperado": 81.31,
    "percentual_escrita_no_esperado": 76.77,
    "percentual_matematica_no_esperado": 72.22
  },
  "itens": [
    {
      "nivel": "municipio",
      "id": "d973590a-b783-490c-825b-a455012462e0",
      "nome": "Cidade BI (RJ)",
      "total_registros": 3,
      "total_alunos": 57,
      "percentual_leitura_no_esperado": 70.18,
      "percentual_escrita_no_esperado": 64.91,
      "percentual_matematica_no_esperado": 59.65
    }
  ]
}
```

## Testes
Na pasta `backend`:

```powershell
python -m pytest -q
```

Arquivos de teste por dominio:
- `tests/test_health.py`
- `tests/test_municipios.py`
- `tests/test_escolas.py`
- `tests/test_turmas.py`
- `tests/test_indicadores_trimestrais.py`
- `tests/test_analytics_ima.py`
- `tests/test_analytics_desempenho.py`
- `tests/test_bi_v1.py`

## Troubleshooting (Windows)

### `uvicorn app.main:app --reload` falha
1. Entrar em `backend`.
2. Ativar `venv`.
3. Garantir dependencias instaladas.
4. Rodar:
```powershell
python -m uvicorn app.main:app --reload
```

### `pytest` nao reconhecido
```powershell
python -m pytest -q
```

### Banco com schema antigo
Aplicar migracao e views manualmente:
```powershell
Get-Content .\database\sql\migrate_component_metrics.sql | docker compose exec -T postgres psql -U postgres -d educacao
Get-Content .\database\views\ima_view.sql | docker compose exec -T postgres psql -U postgres -d educacao
Get-Content .\database\views\desempenho_componentes_view.sql | docker compose exec -T postgres psql -U postgres -d educacao
Get-Content .\database\seeds\seed.sql | docker compose exec -T postgres psql -U postgres -d educacao
```

