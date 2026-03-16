# Power BI Desktop - Conexao com API `/bi/v1`

> Status: legado temporario durante a migracao para Metabase (Fase 5.1).
> Manter para operacao paralela e plano de rollback ate cutover oficial.

Guia rapido para conectar o Power BI Desktop nos endpoints da Fase 4.

## Pre-requisitos
- API rodando localmente (exemplo):
```powershell
cd backend
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```
Obs: alternativa (com ambiente ativado):
```powershell
cd backend
python -m uvicorn app.main:app --reload
```
- Endpoints respondendo em `http://127.0.0.1:8000/bi/v1/*`.

## Arquivos prontos
Estes scripts M ja estao prontos no repositorio:
- `scripts/powerbi/bi_v1_hierarquia.pq`
- `scripts/powerbi/bi_v1_indicadores_trimestrais.pq`
- `scripts/powerbi/bi_v1_ima_municipio.pq`

## Como importar no Power BI
1. Abra o Power BI Desktop.
2. Clique em `Transformar dados` > `Editor Avancado`.
3. Apague o conteudo atual e cole um dos scripts `.pq`.
4. Ajuste `BaseUrl` se necessario.
5. Clique em `Concluido` e depois `Fechar e Aplicar`.

## Parametros mais usados
- `BaseUrl`:
  - local: `http://127.0.0.1:8000`
  - api remota: trocar para URL publicada
- `Ano` e `Trimestre` (script de indicadores):
  - usados para filtro da carga incremental/manual
- `GroupBy` (script IMA):
  - `municipio`, `escola` ou `turma`

## Validacao rapida
No terminal:
```powershell
curl "http://127.0.0.1:8000/bi/v1/hierarquia"
curl "http://127.0.0.1:8000/bi/v1/indicadores-trimestrais?ano=2026&trimestre=1"
curl "http://127.0.0.1:8000/bi/v1/ima?group_by=municipio"
```

Se esses 3 retornarem `200`, a conexao no Power BI deve funcionar.
