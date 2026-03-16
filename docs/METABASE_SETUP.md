# Metabase Setup Local (Fase 5.1)

Guia para operar o Metabase OSS localmente com o modelo atual de desempenho por componente.

## Objetivo
- operar BI sem custo de licenca
- usar `vw_desempenho_componentes` como fonte principal
- manter `vw_ima` apenas como fonte legada temporaria

## Pre-requisitos
- Docker Desktop ativo
- Postgres do projeto funcional em `docker compose`
- PowerShell (Windows)

## 1) Configurar variaveis do Metabase
```powershell
Copy-Item .env.example .env
```

## 2) Subir Postgres e provisionar metadata
```powershell
docker compose up -d postgres
.\scripts\provision_metabase_db.ps1
```

## 3) Garantir views analiticas
```powershell
Get-Content .\database\views\ima_view.sql | docker compose exec -T postgres psql -U postgres -d educacao
Get-Content .\database\views\desempenho_componentes_view.sql | docker compose exec -T postgres psql -U postgres -d educacao
```

## 4) Subir Metabase
```powershell
docker compose up -d metabase
docker compose ps
```

## 5) Onboarding inicial
1. Acessar `http://127.0.0.1:3000`.
2. Criar usuario admin local.
3. Adicionar PostgreSQL com:
   - Host: `postgres`
   - Port: `5432`
   - Database: `educacao`
   - Username: `postgres`
   - Password: `postgres`
4. Habilitar sync/scan.

## 6) Modelagem recomendada
Fonte principal:
- `vw_desempenho_componentes`

Fonte legada:
- `vw_ima`

Dimensoes de apoio:
- `municipios`
- `escolas`
- `turmas`
- `indicadores_trimestrais`

Filtros recomendados no dashboard principal:
- `ano`
- `trimestre`
- `ano_escolar`
- `fonte_avaliacao`
- `municipio_nome`

## 7) Dashboard principal recomendado
Colecao:
- `MVP Educacao`

Dashboard:
- `MVP - Desempenho por Componentes`

KPIs:
- `Qtd Linhas`
- `Total Alunos`
- `Percentual no Esperado - Leitura`
- `Percentual no Esperado - Escrita`
- `Percentual no Esperado - Matematica`

Visuais:
- serie temporal por componente
- comparativo por municipio por componente

SQLs de referencia:
- `scripts/metabase/kpi_cards.sql`
- `scripts/metabase/serie_trimestral.sql`
- `scripts/metabase/comparativo_municipio.sql`

## 8) Validacao inicial rapida
1. Metabase abre sem erro.
2. Banco `educacao` conectado.
3. `vw_desempenho_componentes` visivel no data model.
4. Dashboard principal criado e com dados.
5. `vw_ima` permanece disponivel se precisar comparar legado.
