# Operations - Runbook local

## Baseline oficial
Este runbook segue estas referencias como fonte de verdade:
- `README.md`
- `SYSTEM_CONTEXT.md`
- `docs/EDUCATIONAL_DATA_ARCHITECTURE.md`
- `docs/MIGRATION_PLAN_EDUCATIONAL_ARCHITECTURE.md`
- `docs/architecture_decisions/ADR_007` a `ADR_011`

Arquitetura oficial de referencia:
`Municipio -> Escola -> Turma -> Avaliacao -> Indicadores de aprendizagem`

Camada analitica oficial de referencia:
`Avaliacoes da Rede -> fato_aprendizagem -> vw_desempenho_aprendizagem -> Metabase`

## Estado operacional atual
- API atual opera com `municipios`, `escolas`, `turmas` e `indicadores_trimestrais`
- endpoints BI de Fase 4 permanecem ativos para compatibilidade
- Metabase esta em transicao paralela ao Power BI
- a camada `avaliacoes -> fato_aprendizagem -> vw_desempenho_aprendizagem` deve ser implantada por migrations aditivas, sem quebrar o MVP atual

## Pre-requisitos
- Docker Desktop ativo
- Python instalado e acessivel no terminal
- `backend/venv` configurado para desenvolvimento local
- portas livres: `5433` para Postgres, `8000` para API e `3000` para Metabase

## Subir stack containerizada
```powershell
docker compose up -d postgres api
```

Validar a API:
```powershell
.\scripts\smoke_api.ps1
```

Subir Metabase quando necessario:
```powershell
Copy-Item .env.example .env
.\scripts\provision_metabase_db.ps1
docker compose up -d metabase
```

## Desenvolvimento local com hot reload
```powershell
docker compose up -d postgres
docker compose stop api
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Rodar testes:
```powershell
cd backend
python -m pytest -q
```

## Validacoes rapidas
Health e metricas:
```powershell
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/health/dependencies
curl http://127.0.0.1:8000/metrics
```

BI legado atual:
```powershell
curl "http://127.0.0.1:8000/bi/v1/hierarquia"
curl "http://127.0.0.1:8000/bi/v1/indicadores-trimestrais?ano=2026&trimestre=1"
curl "http://127.0.0.1:8000/bi/v1/ima?group_by=municipio"
```

## Banco atual
Aplicar views atuais de BI, quando necessario:
```powershell
Get-Content .\database\views\ima_view.sql | docker compose exec -T postgres psql -U postgres -d educacao
Get-Content .\database\views\desempenho_componentes_view.sql | docker compose exec -T postgres psql -U postgres -d educacao
```

## Banco - proxima camada oficial
A evolucao oficial do banco deve ocorrer na ordem abaixo:
1. `avaliacoes`
2. `avaliacoes.ciclo_avaliativo`
3. `fato_aprendizagem`
4. `vw_desempenho_aprendizagem`

Essa sequencia deve ser aplicada de forma aditiva e com validacao de compatibilidade com endpoints e dashboards atuais.

## Reset completo de ambiente
Atencao: remove dados locais.
```powershell
docker compose down -v
docker compose up -d postgres api
```

## Troubleshooting rapido
### Docker parado
```powershell
docker compose ps
```
Se falhar, abrir Docker Desktop e repetir o comando.

### API nao sobe
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

### Testes falham
```powershell
cd backend
python -m pytest -q
```

### Metabase nao conecta
- confirmar se `postgres` esta rodando
- reprovisionar metadata DB com `scripts/provision_metabase_db.ps1`
- reiniciar o container `metabase`
