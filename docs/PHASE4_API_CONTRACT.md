# Contrato da Fase 4 - BI v1

## Status
- Implementado
- Prefixo oficial: `/bi/v1`
- Fonte de verdade para a camada BI legada consumida por Power BI e compatibilidade de dashboards

## Relacao com a arquitetura oficial
A arquitetura oficial do projeto evolui para incluir:
- `Avaliacao`
- `fato_aprendizagem`
- `vw_desempenho_aprendizagem`

Isso nao invalida o contrato da Fase 4.
Este documento continua valendo para a camada BI legada e para rollback durante a transicao para Metabase.

## Premissas
- read-only
- sem RBAC completo nesta fase
- sem dados individuais de alunos
- sem paginacao
- erros principais: `422` e `500`

## Endpoints
### 1. `GET /bi/v1/hierarquia`
Retorna a hierarquia denormalizada atual do MVP.

Filtros opcionais:
- `municipio_id`
- `escola_id`
- `turma_id`
- `estado`

### 2. `GET /bi/v1/indicadores-trimestrais`
Retorna o fato trimestral legado para BI do MVP.

Filtros opcionais:
- `municipio_id`
- `escola_id`
- `turma_id`
- `ano`
- `trimestre`

### 3. `GET /bi/v1/ima`
Retorna agregacao legada de IMA.

Filtros opcionais:
- `group_by`
- `ano`
- `trimestre`
- `municipio_id`
- `escola_id`
- `turma_id`

## Regras de evolucao
- nao remover campos existentes em `v1`
- novos contratos para a camada `vw_desempenho_aprendizagem` devem nascer em documento proprio
- qualquer evolucao breaking deve abrir `v2`

## Observacao
Este contrato nao deve ser confundido com o contrato futuro da camada analitica `fato_aprendizagem -> vw_desempenho_aprendizagem`.
