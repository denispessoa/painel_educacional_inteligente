# Metabase - Queries base do dashboard principal

Consultas SQL de referencia para montar o dashboard principal:
- `MVP - Desempenho por Componentes`

Dashboard legado temporario:
- `MVP - Alfabetizacao e IMA`

## Fonte principal
- `vw_desempenho_componentes`

## Fonte legada
- `vw_ima`

## Arquivos
- `kpi_cards.sql`
  - consultas dos cards de KPI do dashboard principal
- `serie_trimestral.sql`
  - serie temporal por componente
- `comparativo_municipio.sql`
  - comparativo por municipio por componente

## Uso sugerido
1. No Metabase, criar uma `Question` SQL para cada consulta.
2. Salvar na colecao `MVP Educacao`.
3. Adicionar as perguntas no dashboard `MVP - Desempenho por Componentes`.
4. Configurar filtros globais do dashboard:
   - `ano`
   - `trimestre`
   - `ano_escolar`
   - `fonte_avaliacao`
   - `municipio_nome`

## Parametros dos SQLs
- `{{ano}}` (numero)
- `{{trimestre}}` (numero)
- `{{ano_escolar}}` (numero)
- `{{fonte_avaliacao}}` (texto)
- `{{municipio_nome}}` (texto)

## Observacao sobre o eixo X
No card `Serie Trimestral por Componentes`, use a coluna `periodo` (`2025 T1`, `2025 T2` etc.) no eixo X.

## Observacao sobre o IMA
`IMA` ainda pode ser mantido em cards secundarios usando `vw_ima`, mas nao deve ser o destaque do dashboard principal.
