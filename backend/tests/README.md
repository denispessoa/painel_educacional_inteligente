# Tests - Estrategia e execucao

## Objetivo
Documentar a estrategia de testes do backend do MVP e a evolucao esperada para a nova arquitetura.

## Estado atual
- testes automatizados cobrem recursos atuais do MVP
- a suite valida CRUD, contratos HTTP e regressao basica dos endpoints existentes
- a nova camada `avaliacoes -> fato_aprendizagem -> vw_desempenho_aprendizagem` ainda precisa de lote proprio de testes quando for consolidada no backend

## Executar a suite
```powershell
cd backend
python -m pytest -q
```

## Principios
- manter testes de regressao das fases 1 a 4 verdes
- tratar migrations novas como aditivas
- nao quebrar endpoints atuais durante a evolucao da arquitetura

## Proxima cobertura necessaria
Quando a arquitetura oficial entrar no backend, adicionar testes para:
- `avaliacoes`
- `ciclo_avaliativo`
- `fato_aprendizagem`
- `vw_desempenho_aprendizagem`
- integridade entre camada operacional e camada analitica
