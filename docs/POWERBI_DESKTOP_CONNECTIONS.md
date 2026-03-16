# Power BI Desktop - Conexoes legadas

## Status
Power BI permanece como camada legada temporaria para operacao paralela e rollback.

## Baseline oficial
Arquitetura-alvo de BI:
`Avaliacoes da Rede -> fato_aprendizagem -> vw_desempenho_aprendizagem -> Metabase`

## Uso atual
Enquanto a arquitetura oficial nao estiver completa em producao local:
- Power BI pode continuar consumindo `/bi/v1/*`
- serve para validacao cruzada com o Metabase
- serve como fallback operacional

## Pre-requisitos
- API local em execucao
- endpoints `/bi/v1/*` respondendo `200`
- Power BI Desktop instalado

## Subir API local
```powershell
cd backend
python -m uvicorn app.main:app --reload
```

## Scripts disponiveis
- `scripts/powerbi/bi_v1_hierarquia.pq`
- `scripts/powerbi/bi_v1_indicadores_trimestrais.pq`
- `scripts/powerbi/bi_v1_ima_municipio.pq`

## Importacao no Power BI
1. abrir `Transformar dados`
2. abrir `Editor Avancado`
3. colar o script `.pq`
4. ajustar `BaseUrl` se necessario
5. aplicar

## Validacao rapida
```powershell
curl "http://127.0.0.1:8000/bi/v1/hierarquia"
curl "http://127.0.0.1:8000/bi/v1/indicadores-trimestrais?ano=2026&trimestre=1"
curl "http://127.0.0.1:8000/bi/v1/ima?group_by=municipio"
```

## Observacao de futuro
Quando a camada `vw_desempenho_aprendizagem` estiver operacional, abrir contrato e conector especificos para essa nova fonte, sem quebrar o uso legado enquanto durar a transicao.
