# Database - Bootstrap e operacao

## Baseline oficial
Arquitetura de dados oficial do projeto:
`Municipio -> Escola -> Turma -> Avaliacao -> Indicadores de aprendizagem`

Camada analitica oficial de referencia:
`avaliacoes -> fato_aprendizagem -> vw_desempenho_aprendizagem`

## Estado atual do banco
- schema operacional principal do MVP segue em `database/sql/schema.sql`
- tabelas atuais do MVP permanecem ativas
- views de BI atuais continuam dando suporte ao dashboard do MVP
- a camada oficial `avaliacoes -> fato_aprendizagem -> vw_desempenho_aprendizagem` deve entrar por migrations aditivas, sem remover estruturas existentes

## Artefatos principais
- `sql/schema.sql`
  - bootstrap estrutural atual do MVP
- `seeds/seed.sql`
  - dados demo e operacionais de apoio
- `views/ima_view.sql`
  - view legada de IMA
- `views/desempenho_componentes_view.sql`
  - view operacional atual do dashboard em Metabase
- `migrations/`
  - lote de evolucao da arquitetura educacional

## Ordem recomendada de uso hoje
1. aplicar `sql/schema.sql` em ambiente novo
2. aplicar `seeds/seed.sql` quando precisar de dados demo
3. aplicar views atuais de BI
4. preparar migrations da nova camada oficial somente quando o lote `avaliacoes + ciclo_avaliativo + fato_aprendizagem + vw_desempenho_aprendizagem` estiver coerente e validado

## Aplicacao manual das views atuais
```powershell
Get-Content .\database\views\ima_view.sql | docker compose exec -T postgres psql -U postgres -d educacao
Get-Content .\database\views\desempenho_componentes_view.sql | docker compose exec -T postgres psql -U postgres -d educacao
```

## Principios de migracao
- migrations sempre aditivas
- nao remover tabelas existentes
- nao quebrar endpoints atuais
- manter compatibilidade com dashboards existentes

## Observacao
`fato_aprendizagem` e `vw_desempenho_aprendizagem` pertencem ao baseline oficial do projeto, mas a implantacao definitiva deve respeitar o plano em `docs/MIGRATION_PLAN_EDUCATIONAL_ARCHITECTURE.md`.
