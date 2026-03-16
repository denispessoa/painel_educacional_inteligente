# Arquitetura interna da API

## Baseline oficial
A arquitetura-alvo do projeto considera:
- `Avaliacao`
- `fato_aprendizagem`
- `vw_desempenho_aprendizagem`
- referencias pedagogicas rastreaveis

## Estado atual implementado
- `main.py`: bootstrap FastAPI e registro de routers atuais
- `db.py`: engine, session e dependencia de banco
- `models.py`: entidades atuais do MVP
- `schemas.py`: contratos de entrada e saida atuais
- `crud.py`: consultas e agregacoes do MVP
- `routers/`: camada HTTP atual

## Fluxo atual de request
1. request entra no router
2. FastAPI valida query ou body
3. router chama `crud.py`
4. `crud.py` executa operacao SQLAlchemy
5. router retorna response model e status HTTP

## Convencoes
- rotas flat com filtros por query string
- IDs em UUID nas entidades operacionais atuais
- sem paginacao nesta etapa do MVP
- sem dados individuais de alunos
- erros principais: `422`, `404`, `409`

## Direcao de evolucao
Quando `avaliacoes` entrar:
- criar modelo, schema e router dedicados
- manter compatibilidade com os recursos atuais
- tratar `fato_aprendizagem` como camada analitica agregada
- expor `vw_desempenho_aprendizagem` para BI e diagnostico, nao como substituto bruto do modelo operacional
