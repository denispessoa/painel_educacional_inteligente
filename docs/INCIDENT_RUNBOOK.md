# Runbook de Incidentes (Fase 5)

Guia rapido para resposta inicial de incidentes operacionais da API e banco.

## Objetivos operacionais
- `RTO` alvo: ate 60 minutos para restaurar API/banco.
- `RPO` alvo: ate 24 horas (backup diario).

## Sinais de alerta minimos
- Falha em `GET /health` (API indisponivel).
- Falha em `GET /health/dependencies` (dependencias degradadas).
- Crescimento de `5xx` em `GET /metrics`.

## Incidente 1: API fora do ar
1. Verificar processo API:
```powershell
Get-Process | Where-Object { $_.ProcessName -like '*python*' -or $_.ProcessName -like '*uvicorn*' }
```
Se estiver usando container:
```powershell
docker compose ps
docker compose logs -f api
```
2. Validar health:
```powershell
curl http://127.0.0.1:8000/health
```
3. Reiniciar API:
```powershell
docker compose restart api
```
Se a API estiver rodando localmente em vez de container:
```powershell
cd backend
python -m uvicorn app.main:app --reload
```

## Incidente 2: banco indisponivel
1. Verificar container:
```powershell
docker compose ps
```
2. Ler logs:
```powershell
docker compose logs -f postgres
```
3. Reiniciar Postgres:
```powershell
docker compose restart postgres
```
4. Confirmar dependencia:
```powershell
curl http://127.0.0.1:8000/health/dependencies
```

## Incidente 3: degradacao de endpoints BI
1. Testar endpoints principais:
```powershell
curl "http://127.0.0.1:8000/bi/v1/hierarquia"
curl "http://127.0.0.1:8000/bi/v1/indicadores-trimestrais?ano=2026&trimestre=1"
curl "http://127.0.0.1:8000/bi/v1/ima?group_by=municipio&ano=2026&trimestre=1"
```
2. Validar view analitica (Postgres):
```powershell
Get-Content .\database\views\ima_view.sql | docker compose exec -T postgres psql -U postgres -d educacao
```
3. Revalidar endpoints BI apos reaplicar a view.

## Incidente 4: Metabase indisponivel
1. Verificar container:
```powershell
docker compose ps
```
2. Ler logs do Metabase:
```powershell
docker compose logs -f metabase
```
3. Validar metadata DB:
```powershell
.\scripts\provision_metabase_db.ps1
```
4. Reiniciar Metabase:
```powershell
docker compose restart metabase
```
5. Se nao estabilizar, executar rollback operacional para Power BI legado temporario.

## Backup e restore
Gerar backup SQL:
```powershell
.\scripts\backup_postgres.ps1
```

Restaurar backup:
```powershell
.\scripts\restore_postgres.ps1 -InputFile .\export\educacao_backup_YYYYMMDD_HHMMSS.sql
```

## Encerramento do incidente
1. Registrar causa raiz.
2. Registrar horario de inicio/fim e impacto.
3. Atualizar acao preventiva em `docs/OPERATIONS.md` quando aplicavel.
