# Backend Tests - Estrategia e execucao

## Objetivo
Garantir comportamento esperado das fases 1-3 com foco em:
- contrato HTTP
- regras de validacao
- integridade referencial
- calculo de indicadores e IMA

## Estrutura atual
- `conftest.py`
  - cria ambiente de teste com SQLite in-memory
  - habilita `PRAGMA foreign_keys=ON`
  - override de dependencia `get_db` para cada teste
- `test_health.py`
  - health endpoint
- `test_municipios.py`
  - CRUD e conflitos por dependencia com escolas
- `test_escolas.py`
  - CRUD e conflitos por dependencia com turmas
- `test_turmas.py`
  - CRUD base
- `test_indicadores_trimestrais.py`
  - validacoes, duplicidade por periodo, calculo de percentuais
- `test_analytics_ima.py`
  - agregacoes e filtros de analytics IMA

## Como executar
Na pasta `backend`:
```powershell
python -m pytest -q
```

Executar apenas um arquivo:
```powershell
python -m pytest tests/test_indicadores_trimestrais.py -q
```

Executar um teste especifico:
```powershell
python -m pytest tests/test_analytics_ima.py::test_analytics_ima_filter_by_period -q
```

## Cobertura funcional esperada por fase
- Fase 1:
  - health
  - CRUD de municipios, escolas e turmas
  - erros `404`, `409`, `422`
- Fase 2:
  - CRUD de indicadores trimestrais
  - validacoes de faixa e consistencia de totais
  - unicidade de `turma+ano+trimestre`
- Fase 3:
  - endpoint `/analytics/ima`
  - filtros por periodo e hierarquia
  - agregacao por `municipio`, `escola` e `turma`

## Regras para novos testes
- Sempre isolar teste com setup no proprio caso ou helper local.
- Ao incluir novo endpoint, adicionar:
  1. caso feliz
  2. pelo menos 1 caso de validacao `422`
  3. caso `404` quando aplicavel
  4. caso `409` quando aplicavel
