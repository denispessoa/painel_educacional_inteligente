# Essencia do Projeto (Contexto para IA)

Use este arquivo como contexto base para pedir insights tecnicos, de produto e de operacao em outras IAs.

## 1) Resumo executivo
- Projeto: Plataforma Municipal de Inteligencia Educacional (MVP).
- Objetivo: apoiar gestao educacional municipal com dados agregados de desempenho escolar.
- Regra central: sem dados individuais de alunos.
- Stack principal: FastAPI + PostgreSQL + Metabase OSS (Power BI legado temporario).
- Hierarquia: `Municipio -> Escola -> Turma -> Indicadores`.

## 2) Modelo semantico atual
- `1o-5o ano`: base operacional `CNCA`.
- `6o-9o ano`: base operacional `MEC Anos Finais BNCC`.
- `Saeb`: referencia complementar de governanca e comparabilidade.
- metricas principais:
  - `percentual no esperado - leitura`
  - `percentual no esperado - escrita`
  - `percentual no esperado - matematica`
- criterio de atingimento:
  - `Proficiente + Avancado`
- `IMA` e legado temporario.

## 3) Ativo estrategico novo
O projeto passou a manter um documento-base de convergencia entre avaliacao externa, BNCC e futura matriz curricular da rede:
- `docs/CONVERGENCIA_AVALIACOES_BNCC_REDE.md`

Esse artefato existe para preparar adequacao futura a diferentes redes sem improvisar equivalencias entre descritores, habilidades e curriculo local.

Trilha futura ja registrada:
- `fluencia em leitura` como projeto avaliativo proprio, inicialmente ancorado no bloco `CNCA/CAEd` de `2o-5o ano`

## 4) O que ja foi entregue
- Fase 1: CRUD de `municipios`, `escolas`, `turmas`.
- Fase 2: `indicadores-trimestrais`.
- Fase 3: analytics no backend.
- Fase 4: endpoints BI read-only em `/bi/v1/*`.
- Fase 5: baseline operacional, observabilidade, backup/restore e Metabase OSS.
- Revisao semantica atual:
  - modelo por componente com `ano_escolar` e `fonte_avaliacao`
  - `vw_desempenho_componentes`
  - endpoints novos `/analytics/desempenho`, `/bi/v1/indicadores-componentes`, `/bi/v1/desempenho`

## 5) Modelo de dados (visao curta)
- Entidades: `Municipio`, `Escola`, `Turma`, `IndicadorTrimestral`.
- Campos chave do indicador:
  - `ano`, `trimestre`
  - `ano_escolar`
  - `fonte_avaliacao`
  - `total_alunos`
  - `atingiu_esperado_leitura`
  - `atingiu_esperado_escrita`
  - `atingiu_esperado_matematica`
  - `percentual_leitura`
  - `percentual_escrita`
  - `percentual_matematica`
- Compatibilidade temporaria:
  - `alfabetizados_leitura`
  - `alfabetizados_escrita`

## 6) Contratos de API (visao curta)
- CRUD base:
  - `/municipios`
  - `/escolas`
  - `/turmas`
  - `/indicadores-trimestrais`
- Analytics principal:
  - `GET /analytics/desempenho`
- BI principal:
  - `GET /bi/v1/hierarquia`
  - `GET /bi/v1/indicadores-componentes`
  - `GET /bi/v1/desempenho`
- Legado:
  - `GET /analytics/ima`
  - `GET /bi/v1/indicadores-trimestrais`
  - `GET /bi/v1/ima`
  - `vw_ima`

## 7) Estado operacional atual
- Testes backend: `50 passed`.
- Banco local alinhado ao novo schema.
- Dataset demo local:
  - `72` linhas em `vw_desempenho_componentes`
  - `1o-9o ano`
  - `CNCA` e `MEC Anos Finais BNCC`
- Metabase OSS local segue como camada BI principal em evolucao.
- Proximo passo natural ja registrado:
  - migrar a dashboard do Metabase para o modelo de componentes.

## 8) Riscos atuais
- `IMA` ainda existe e pode induzir leitura errada se continuar em destaque no BI.
- Comparacoes entre anos escolares diferentes exigem contexto de etapa/fonte.
- `escrita` demanda convergencia curricular mediada da rede, nao apenas equivalencia automatica com descritores externos.
- `fluencia` ainda nao possui contrato de dados proprio no projeto e nao deve ser misturada com os percentuais atuais de leitura.

## 9) Proximos passos naturais
1. Finalizar a convergencia BNCC/rede com a equipe pedagogica quando a matriz curricular municipal estiver versionada.
2. Concluir o dashboard do Metabase com foco em componentes.
3. Adicionar catalogo de metricas e dicionario de dados.
4. Estruturar o projeto futuro de `fluencia em leitura` com contrato proprio.
5. Evoluir governanca e qualidade de dados.
