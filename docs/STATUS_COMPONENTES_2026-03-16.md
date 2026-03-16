# Status do Desenvolvimento - Modelo por Componentes

Data de referencia: `2026-03-16`

## Checkpoint registrado
- commit de base documental: `3780bc7 docs: add saeb and cnca reference base`
- commit de implementacao estrutural: `3118c4a feat: replace ima with component metrics across cnca and mec anos finais`

## Estado atual do produto
- backend migrado para o modelo por componente
- `ano_escolar` ativo de `1o` a `9o`
- `fonte_avaliacao` ativa:
  - `cnca` para `1o-5o`
  - `mec_anos_finais_bncc` para `6o-9o`
- metricas principais:
  - `percentual_leitura`
  - `percentual_escrita`
  - `percentual_matematica`
- `IMA` mantido apenas como legado temporario

## Estado tecnico validado
- testes backend: `50 passed`
- views principais:
  - `vw_desempenho_componentes`
  - `vw_ima` (legado)
- dataset demo atual:
  - `72` linhas
  - `1o-9o ano`
  - `2025` e `2026`
  - `CNCA`: `40` linhas
  - `MEC Anos Finais BNCC`: `32` linhas

## Endpoints principais ativos
- `GET /analytics/desempenho`
- `GET /bi/v1/indicadores-componentes`
- `GET /bi/v1/desempenho`

## Endpoints legados mantidos
- `GET /analytics/ima`
- `GET /bi/v1/indicadores-trimestrais`
- `GET /bi/v1/ima`

## Proximo passo natural registrado
Atualizar a dashboard do Metabase para o modelo principal de desempenho por componentes, usando:
- `vw_desempenho_componentes`
- `scripts/metabase/kpi_cards.sql`
- `scripts/metabase/serie_trimestral.sql`
- `scripts/metabase/comparativo_municipio.sql`

## Desvio planejado antes do dashboard
Antes de executar esse proximo passo, o projeto vai consolidar a convergencia entre:
- descritores/habilidades de `CNCA/CAEd`
- descritores/habilidades da `Avaliacao Continua da Aprendizagem nos Anos Finais`
- descritores/habilidades do `Saeb`
- habilidades da `BNCC`
- futura matriz curricular da rede municipal

Documento-base dessa etapa:
- `docs/CONVERGENCIA_AVALIACOES_BNCC_REDE.md`
