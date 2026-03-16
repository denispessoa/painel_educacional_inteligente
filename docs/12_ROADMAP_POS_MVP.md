# Roadmap Pos-MVP

## Baseline oficial
Este roadmap segue:
- `README.md`
- `SYSTEM_CONTEXT.md`
- `docs/EDUCATIONAL_DATA_ARCHITECTURE.md`
- `docs/MIGRATION_PLAN_EDUCATIONAL_ARCHITECTURE.md`
- ADRs `007` a `011`

## Principios de evolucao
- nao remover estruturas existentes do MVP
- preferir migrations aditivas
- manter dashboards atuais operacionais durante a transicao
- consolidar a avaliacao da rede como fonte primaria
- separar claramente camada operacional, camada analitica e referencias pedagogicas

## Fase 5
- estabilizacao operacional
- backup e restore
- CI de backend
- observabilidade minima
- Metabase OSS em paralelo ao Power BI

## Fase 6 - Camada Avaliacao
- criar `avaliacoes`
- introduzir `fonte_avaliacao`
- introduzir `ciclo_avaliativo`
- manter compatibilidade com `indicadores_trimestrais`

## Fase 7 - Camada analitica de aprendizagem
- consolidar `fato_aprendizagem`
- consolidar `vw_desempenho_aprendizagem`
- conectar Metabase na nova view
- manter Power BI legado durante a transicao

## Fase 8 - Referencias pedagogicas e diagnostico
- estruturar mapa de descritores
- conectar matriz, blueprint e descritores da rede
- preparar camada semantica para diagnostico pedagogico
- manter banco de itens fora do escopo imediato

## Frentes permanentes
1. Infraestrutura tecnica
2. Camada analitica
3. Referencias pedagogicas
