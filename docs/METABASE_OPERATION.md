# Metabase - Operacao Local

## Rotina basica
Subir stack:
```powershell
docker compose up -d postgres metabase
```

Garantir views:
```powershell
Get-Content .\database\views\ima_view.sql | docker compose exec -T postgres psql -U postgres -d educacao
Get-Content .\database\views\desempenho_componentes_view.sql | docker compose exec -T postgres psql -U postgres -d educacao
```

## Validacoes operacionais
- `vw_desempenho_componentes` deve estar sincronizada no Metabase.
- `vw_ima` deve permanecer disponivel apenas para comparacao legada.
- dashboard principal esperado:
  - `MVP - Desempenho por Componentes`

## Logs
```powershell
docker compose logs -f metabase
docker compose logs -f postgres
```

## Reinicio
```powershell
docker compose restart metabase
```

## Quando a base mudar de contrato
Se alterar schema, views ou seed no repositorio:
```powershell
Get-Content .\database\sql\migrate_component_metrics.sql | docker compose exec -T postgres psql -U postgres -d educacao
Get-Content .\database\views\ima_view.sql | docker compose exec -T postgres psql -U postgres -d educacao
Get-Content .\database\views\desempenho_componentes_view.sql | docker compose exec -T postgres psql -U postgres -d educacao
Get-Content .\database\seeds\seed.sql | docker compose exec -T postgres psql -U postgres -d educacao
```
