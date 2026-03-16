# Metabase Setup - Local

## Objetivo
Subir o Metabase OSS localmente para a camada BI do MVP, mantendo compatibilidade com a arquitetura oficial definida no projeto.

## Baseline oficial
Arquitetura alvo:
`Municipio -> Escola -> Turma -> Avaliacao -> Indicadores`

Pipeline analitico alvo:
`Avaliacoes da Rede -> fato_aprendizagem -> vw_desempenho_aprendizagem -> Metabase`

## Estado atual
- Metabase pode ser usado hoje com as views operacionais existentes do MVP
- `vw_desempenho_aprendizagem` faz parte da arquitetura oficial e deve entrar de forma aditiva, sem interromper o uso atual do BI
- Power BI segue documentado como legado temporario para rollback

## Pre-requisitos
- Docker Desktop ativo
- `.env` criado a partir de `.env.example`
- Postgres local do projeto disponivel

## Provisionar metadata DB
```powershell
Copy-Item .env.example .env
.\scripts\provision_metabase_db.ps1
```

## Subir Metabase
```powershell
docker compose up -d metabase
```

Acesso local:
- `http://127.0.0.1:3000`

## Conectar o banco educacao
No onboarding do Metabase:
- Database type: `PostgreSQL`
- Host: `postgres`
- Port: `5432`
- Database name: `educacao`
- User: `postgres`
- Password: `postgres`

## Fontes e objetos recomendados
### Camada atual do MVP
- `vw_ima`
- `vw_desempenho_componentes`
- tabelas operacionais (`municipios`, `escolas`, `turmas`, `indicadores_trimestrais`)

### Camada oficial de evolucao
Quando implantada no banco:
- `avaliacoes`
- `fato_aprendizagem`
- `vw_desempenho_aprendizagem`

## Sincronizacao apos mudancas
No Metabase:
1. `Admin` -> `Databases`
2. selecionar `educacao`
3. executar `Sync database schema now`
4. executar `Re-scan field values now`

## Observacao importante
Nao usar este documento para afirmar que a camada `avaliacoes -> fato_aprendizagem -> vw_desempenho_aprendizagem` ja esta completa em producao local. Ela e a baseline oficial de evolucao e deve ser consolidada pelas migrations oficiais antes de virar dependencia primaria do dashboard.
