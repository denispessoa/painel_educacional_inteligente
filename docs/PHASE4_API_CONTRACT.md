# Contrato de API - Fase 4 (Power BI Read-Only)

## Status
- Implementado em `2026-03-02`.
- Router ativo: `/bi/v1`.
- Este documento permanece como fonte de verdade do contrato `v1`.

## Objetivo
Definir, antes de implementacao, os endpoints de leitura para consumo do Power BI.

## Premissas fixas
- Sem RBAC completo nesta fase.
- Sem dados individuais de alunos.
- Endpoints read-only.
- Versao inicial: `v1`.
- Sem paginacao na Fase 4 (mesmo padrao das fases anteriores).

## Versionamento
- Prefixo obrigatorio: `/bi/v1`.
- Mudanca breaking gera nova versao (`/bi/v2`).
- Em `v1`, permitido apenas adicionar campos novos sem remover/renomear campos existentes.

## Endpoints definidos

## 1) `GET /bi/v1/hierarquia`
Retorna dimensao denormalizada da hierarquia municipal.

### Filtros opcionais
- `municipio_id` (UUID)
- `escola_id` (UUID)
- `turma_id` (UUID)
- `estado` (string de 2 letras)

### Response `200`
Array simples:
```json
[
  {
    "municipio_id": "uuid",
    "municipio_nome": "Mendes",
    "municipio_estado": "RJ",
    "escola_id": "uuid",
    "escola_nome": "Escola A",
    "turma_id": "uuid",
    "turma_nome": "Turma 1"
  }
]
```

### Erros
- `422` para filtro invalido

## 2) `GET /bi/v1/indicadores-trimestrais`
Retorna fato trimestral completo, pronto para carga no BI.

### Filtros opcionais
- `municipio_id` (UUID)
- `escola_id` (UUID)
- `turma_id` (UUID)
- `ano` (`2000..2100`)
- `trimestre` (`1..4`)

### Response `200`
Array simples:
```json
[
  {
    "indicador_id": "uuid",
    "ano": 2026,
    "trimestre": 1,
    "turma_id": "uuid",
    "turma_nome": "Turma 1",
    "escola_id": "uuid",
    "escola_nome": "Escola A",
    "municipio_id": "uuid",
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

### Fonte de dados
- Prioridade: view `vw_ima` (`database/views/ima_view.sql`).
- Fallback: join equivalente nas tabelas base.

### Erros
- `422` para filtro invalido

## 3) `GET /bi/v1/ima`
Retorna agregacao de IMA por nivel.

### Filtros opcionais
- `group_by`: `municipio` (default), `escola`, `turma`
- `ano` (`2000..2100`)
- `trimestre` (`1..4`)
- `municipio_id` (UUID)
- `escola_id` (UUID)
- `turma_id` (UUID)

### Response `200`
```json
{
  "group_by": "municipio",
  "filtros": {
    "ano": 2026,
    "trimestre": 1,
    "municipio_id": null,
    "escola_id": null,
    "turma_id": null
  },
  "resumo": {
    "total_registros": 10,
    "total_alunos": 250,
    "percentual_leitura_medio": 62.4,
    "percentual_escrita_medio": 58.1,
    "ima_medio": 60.25
  },
  "itens": [
    {
      "nivel": "municipio",
      "id": "uuid",
      "nome": "Mendes (RJ)",
      "total_registros": 4,
      "total_alunos": 120,
      "percentual_leitura_medio": 61.7,
      "percentual_escrita_medio": 57.2,
      "ima_medio": 59.45
    }
  ]
}
```

### Erros
- `422` para `group_by` invalido ou filtros fora da faixa

## Contrato de erro padrao (Fase 4)
- `422`: validacao de query params
- `500`: erro interno inesperado

Observacao:
- `404` nao e esperado nos endpoints de lista/agregacao.
- `409` nao se aplica por serem endpoints read-only.

## Regras de ordenacao
- `/bi/v1/hierarquia`: ordenar por `municipio_nome`, `escola_nome`, `turma_nome`.
- `/bi/v1/indicadores-trimestrais`: ordenar por `ano DESC`, `trimestre DESC`, `municipio_nome`, `escola_nome`, `turma_nome`.
- `/bi/v1/ima`: ordenar `itens` por `nome`.

## Cenarios de aceite para implementacao
1. Cada endpoint retorna `200` com payload no formato definido.
2. Filtros invalidos retornam `422`.
3. Dados retornados nao contem informacao individual de aluno.
4. `/bi/v1/indicadores-trimestrais` retorna exatamente os campos de contrato.
5. `/bi/v1/ima` mantem consistencia da formula:
   - `ima = (percentual_leitura_medio + percentual_escrita_medio) / 2`

## Fora do escopo da Fase 4
- Escrita/edicao de dados via endpoints BI.
- Autenticacao/autorizacao avancada.
- Paginacao.
