# Metabase Operation

## Objetivo
Documentar a operacao diaria do Metabase no projeto durante a transicao Power BI -> Metabase OSS.

## Baseline oficial
- Metabase e a camada BI principal alvo do projeto
- a fonte primaria de monitoramento e a avaliacao da rede
- a camada analitica oficial de referencia e `fato_aprendizagem -> vw_desempenho_aprendizagem`

## Estado atual de operacao
- o dashboard MVP pode operar com views ja disponiveis no banco
- Power BI permanece como fallback temporario
- a nova camada analitica oficial ainda deve ser consolidada sem quebrar o MVP atual

## Operacao diaria
### Subir Metabase
```powershell
docker compose up -d metabase
```

### Parar Metabase
```powershell
docker compose stop metabase
```

### Ver logs
```powershell
docker compose logs -f metabase
```

## Rotina recomendada
1. subir `postgres`
2. validar API e banco
3. subir `metabase`
4. sincronizar schema apos mudancas de banco
5. validar dashboards principais

## Fontes atuais para dashboard
- `vw_ima`
- `vw_desempenho_componentes`
- consultas SQL em `scripts/metabase/`

## Fontes oficiais de evolucao
- `avaliacoes`
- `fato_aprendizagem`
- `vw_desempenho_aprendizagem`

## Validacoes operacionais
- sem erro no carregamento do dashboard
- filtros respondendo com numeros coerentes
- comparacao SQL x Metabase validada no checklist

## Backup e restore
Usar scripts:
- `scripts/backup_metabase_db.ps1`
- `scripts/restore_metabase_db.ps1`

## Troubleshooting
### Dashboard vazio
- verificar se o banco `educacao` esta acessivel
- ressincronizar schema no Metabase
- validar se a view consultada existe no Postgres

### Filtros nao atualizam
- executar `Re-scan field values now`
- revisar se o card usa os parametros corretos
- validar a consulta SQL fora do Metabase

### Mudanca na arquitetura analitica
Quando a camada oficial `vw_desempenho_aprendizagem` entrar, revisar:
- colecoes
- cards
- filtros globais
- checklist de paridade
