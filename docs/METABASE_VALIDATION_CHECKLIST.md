# Metabase Validation Checklist

## Objetivo
Validar a paridade entre SQL e Metabase durante a transicao do BI do projeto.

## Baseline oficial
A arquitetura oficial do BI deve convergir para:
`Avaliacoes da Rede -> fato_aprendizagem -> vw_desempenho_aprendizagem -> Metabase`

## Estado atual
A validacao ainda pode usar a camada atual do MVP (`vw_ima`, `vw_desempenho_componentes`) enquanto a camada oficial nao estiver totalmente implantada.

## Checklist atual
### 1. Infraestrutura
- `postgres` em execucao
- `api` respondendo `200` em `/health`
- `metabase` acessivel em `http://127.0.0.1:3000`

### 2. Banco
- a view usada no dashboard existe no Postgres
- consulta SQL direta retorna dados
- filtros de `ano`, `trimestre` e demais dimensoes retornam subconjuntos coerentes

### 3. Metabase
- sincronizacao de schema concluida
- sem erro de refresh
- filtros globais respondem corretamente
- cards KPI exibem os mesmos numeros da consulta SQL de referencia

### 4. Camada oficial futura
Quando `vw_desempenho_aprendizagem` estiver pronta, validar obrigatoriamente:
- colunas: `ano`, `trimestre`, `ciclo_avaliativo`, `ano_escolar`, `componente`, `dominio`, `descritor`, `percentual`
- consistencia entre `avaliacoes`, `fato_aprendizagem` e a view
- comparacao entre dashboards atuais e novos dashboards de aprendizagem

## Consultas de referencia
Camada atual:
```powershell
docker compose exec -T postgres psql -U postgres -d educacao -c "select count(*) from vw_desempenho_componentes;"
```

Camada oficial futura:
```powershell
docker compose exec -T postgres psql -U postgres -d educacao -c "select * from vw_desempenho_aprendizagem limit 10;"
```

## Criterio de aceite
- o Metabase exibe os mesmos valores do SQL de referencia
- os filtros nao quebram cards nem graficos
- nenhuma validacao depende de dado individual de aluno
