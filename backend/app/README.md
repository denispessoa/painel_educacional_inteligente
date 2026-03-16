# Backend App - Arquitetura interna

Este diretorio contem o nucleo da API FastAPI do MVP.

## Camadas e responsabilidade
- `main.py`
  - cria instancia FastAPI
  - registra routers
  - executa bootstrap de schema com `Base.metadata.create_all(...)` no startup
  - aplica middleware de observabilidade de requests
- `db.py`
  - define `engine`, `SessionLocal`, `Base` e dependencia `get_db`
  - define URL default do banco
- `observability.py`
  - log estruturado JSON para eventos da API
  - metricas basicas (`requests_total`, `2xx/4xx/5xx`, latencia media)
- `models.py`
  - mapeamento ORM SQLAlchemy 2.0
  - entidades: `Municipio`, `Escola`, `Turma`, `IndicadorTrimestral`
- `schemas.py`
  - contratos de entrada e saida (Pydantic)
  - validacoes de negocio (ex.: limites de `ano`, `trimestre`, alfabetizados <= total)
- `crud.py`
  - consultas e mutacoes no banco
  - calculo de percentuais e agregacao de IMA
- `routers/`
  - camada HTTP
  - mapeia status e mensagens de erro (`422`, `404`, `409`)

## Fluxo de request
1. Request entra no router correspondente.
2. Middleware registra metrica/latencia e log estruturado da chamada.
3. FastAPI valida query/body com schemas.
4. Router executa verificacoes de existencia/dependencia.
5. Router chama funcao em `crud.py`.
6. `crud.py` executa operacao SQLAlchemy com `Session`.
7. Router retorna response model e status HTTP.

## Convencoes do projeto
- Rotas flat com filtros query string (sem rotas aninhadas).
- IDs em UUID.
- Sem paginacao nesta etapa.
- Deletes sao hard delete com bloqueio por dependencia (FK `RESTRICT`).
- Erros:
  - `422` validacao
  - `404` nao encontrado
  - `409` conflito de integridade/regra

## Regra de evolucao
- Mudancas de contrato HTTP devem ser refletidas em:
  1. `schemas.py`
  2. router impactado
  3. testes do recurso
  4. `backend/README.md`
  5. `docs/PHASE4_API_CONTRACT.md` (quando envolver endpoints BI)

## Observacao de banco
- Durante o MVP, nao ha Alembic.
- A base estrutural oficial continua em `database/sql/schema.sql`.
- O `create_all` no startup serve para alinhar ambiente local com modelos atuais.
