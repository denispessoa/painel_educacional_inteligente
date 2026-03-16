# Base de Referencia das Metricas por Componente

## Objetivo
Registrar a base pedagogica e semantica que orienta o modelo atual de `leitura`, `escrita` e `matematica` do produto.

## Decisao consolidada
- `1o-5o ano`: referencia operacional `CNCA`
- `6o-9o ano`: referencia operacional `MEC Anos Finais BNCC`
- `Saeb`: referencia complementar de governanca, comparabilidade e interpretacao de bandas
- metrica principal do produto:
  - `percentual de estudantes no esperado` por componente
- `IMA` permanece apenas como indicador legado de compatibilidade por `1 ciclo`

## Componentes validos no modelo
- `leitura`
- `escrita`
- `matematica`

Esses tres componentes sao tratados como metricas independentes, sempre contextualizadas por:
- `ano_escolar`
- `fonte_avaliacao`
- `ano`
- `trimestre`

## Corte de desempenho adotado
- `atingiu o esperado = Proficiente + Avancado`

## Normalizacao interna de bandas
O produto usa uma taxonomia interna comum:
- `abaixo_basico`
- `basico`
- `proficiente`
- `avancado`

Para referencias com niveis numerados:
- escalas com `8 niveis`: `1-2`, `3-4`, `5-6`, `7-8`
- escalas com `9 niveis`: `1-2`, `3-4`, `5-6`, `7-9`

## Papel de cada referencia

### CNCA (`1o-5o`)
- base operacional dos anos iniciais
- cobre `leitura`, `escrita` e `matematica`
- o `1o ano` ja entra no modelo vigente

Arquivos versionados:
- `docs/references/cnca/CNCAGuiadaAvaliaoContnua.pdf`
- `docs/references/cnca/MEC_2026_CNCA_Av_Cont_Apren_Matriz_Ref.pdf`
- `docs/references/cnca/MEC_2025-Matriz_Anos_Finais.pdf`

### MEC Anos Finais BNCC (`6o-9o`)
- base operacional dos anos finais
- cobre `leitura`, `escrita` e `matematica`
- nao deve ser apresentada como escala oficial Saeb

Arquivo versionado:
- `docs/references/cnca/MEC_2025-Matriz_Anos_Finais.pdf`

### Saeb
- permanece no repositorio como base de comparabilidade e governanca
- ajuda a interpretar a progressao de habilidades e escalas, mas nao e a fonte operacional obrigatoria do modelo atual

Arquivos versionados:
- `docs/references/saeb/matriz_matematica-base-saeb-2001.pdf`
- `docs/references/saeb/matriz_linguaportuguesa-base-saeb-2001.pdf`
- `docs/references/saeb/matriz-de-referencia-de-matematica_BNCC-2018.pdf`
- `docs/references/saeb/matriz-de-referencia-de-linguagens_BNCC-2018.pdf`
- `docs/references/saeb/escala_de_proficiencias_saeb_2025.pdf`

## Mapeamento semantico do modelo
Campos canonicos por registro trimestral:
- `ano_escolar`
- `fonte_avaliacao`
- `atingiu_esperado_leitura`
- `atingiu_esperado_escrita`
- `atingiu_esperado_matematica`
- `percentual_leitura`
- `percentual_escrita`
- `percentual_matematica`

Campos legados mantidos temporariamente:
- `alfabetizados_leitura`
- `alfabetizados_escrita`

Esses campos legados hoje sao aliases de leitura e escrita no esperado. Estao marcados como deprecated.

## Formula das metricas
- `percentual_leitura = atingiu_esperado_leitura / total_alunos * 100`
- `percentual_escrita = atingiu_esperado_escrita / total_alunos * 100`
- `percentual_matematica = atingiu_esperado_matematica / total_alunos * 100`
- se `total_alunos = 0`, todos os percentuais sao `0.00`

## Situacao do IMA
- formula legada: `(percentual_leitura + percentual_escrita) / 2`
- uso permitido: compatibilidade com camada BI antiga
- uso nao recomendado: metrica principal de decisao

## Implicacoes de governanca
Qualquer leitura do dado precisa considerar ao mesmo tempo:
- serie avaliada
- componente
- fonte da matriz
- periodo

Comparacoes brutas entre `2o` e `9o` ano sem contextualizacao de etapa continuam semanticamente fracas, mesmo com a normalizacao interna.

## Proximos passos recomendados
1. Encerrar migracao do dashboard do Metabase para o modelo de componentes.
2. Tratar `IMA` como visual legado, nao como indicador central.
3. Criar catalogo formal de metricas e dicionario de dados na fase de governanca.
4. Se houver necessidade futura de comparabilidade externa forte, introduzir camada explicita de nivel/banda por componente.
