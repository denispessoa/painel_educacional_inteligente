# Scripts Power BI (`.pq`)

Status: legado temporario durante migracao para Metabase.

Consultas M prontas para conectar no namespace `/bi/v1` da API.

## Arquivos
- `bi_v1_hierarquia.pq`
  - dimensao denormalizada municipio/escola/turma
- `bi_v1_indicadores_trimestrais.pq`
  - fato trimestral com filtros de `Ano` e `Trimestre`
- `bi_v1_ima_municipio.pq`
  - agregacao IMA (default `group_by=municipio`)

## Uso
1. Copie o conteudo de um `.pq`.
2. No Power BI Desktop: `Transformar dados` > `Editor Avancado`.
3. Cole o script e ajuste `BaseUrl`/parametros.

## Observacao
- Os scripts usam `Web.Contents` com `RelativePath` e `Query`.
- IDs UUID sao carregados como `text`.
