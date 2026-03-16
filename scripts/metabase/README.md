# Metabase - Queries base do dashboard MVP

Consultas SQL de referencia para montar o dashboard:
- `MVP - Alfabetizacao e IMA`

## Arquivos
- `kpi_cards.sql`
  - consultas dos cards de KPI
- `serie_trimestral.sql`
  - serie temporal por ano/trimestre
- `comparativo_municipio.sql`
  - comparativo por municipio

## Uso sugerido
1. No Metabase, criar uma "Question" SQL para cada consulta.
2. Salvar na colecao `MVP Educacao`.
3. Adicionar as perguntas no dashboard `MVP - Alfabetizacao e IMA`.
4. Configurar filtros globais do dashboard:
   - `ano`
   - `trimestre`
   - `municipio_nome`

## Parametros dos SQLs
Os SQLs usam parametros opcionais do Metabase:
- `{{ano}}` (numero)
- `{{trimestre}}` (numero)
- `{{municipio_nome}}` (texto)

No editor SQL, configure os 3 parametros para cada pergunta antes de salvar.
