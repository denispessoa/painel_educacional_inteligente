# Plano de Implantacao Pos-MVP

## Objetivo
Executar a evolucao da plataforma sem quebrar o MVP atual.

## Baseline oficial
Arquitetura de referencia:
`Municipio -> Escola -> Turma -> Avaliacao -> Indicadores de aprendizagem`

Pipeline analitico de referencia:
`Avaliacoes da Rede -> fato_aprendizagem -> vw_desempenho_aprendizagem -> Metabase`

## Sequencia recomendada
### Etapa 1 - Documentacao e alinhamento
- consolidar `README.md`, `SYSTEM_CONTEXT.md`, `EDUCATIONAL_DATA_ARCHITECTURE.md`, `MIGRATION_PLAN_EDUCATIONAL_ARCHITECTURE.md` e ADRs como fonte de verdade
- alinhar documentacao operacional ao mesmo contrato

### Etapa 2 - Banco
- criar `avaliacoes`
- adicionar `ciclo_avaliativo`
- garantir `fonte_avaliacao`
- manter `municipios`, `escolas`, `turmas` e `indicadores_trimestrais` intactos

### Etapa 3 - Camada analitica
- consolidar `fato_aprendizagem`
- consolidar `vw_desempenho_aprendizagem`
- validar consultas agregadas por `ano`, `trimestre`, `ciclo_avaliativo`, `ano_escolar`, `componente`, `dominio` e `descritor`

### Etapa 4 - BI
- atualizar Metabase para a view oficial
- manter conectores e endpoints legados de Power BI enquanto necessario
- validar paridade SQL x BI

### Etapa 5 - Referencias pedagogicas
- amarrar descritores, matriz, blueprint e curriculo municipal
- preparar catalogo semantico de apoio ao diagnostico

## Regras de seguranca
- migrations sempre aditivas
- sem quebra de endpoints atuais
- sem remocao de tabelas existentes
- sem dados individuais de alunos

## Frentes de trabalho
1. Infraestrutura tecnica (`API + banco + BI`)
2. Camada analitica (`fato_aprendizagem`)
3. Referencias pedagogicas (`matriz`, `blueprint`, `descritores`)
