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
- `IMA` permanece apenas como artefato legado de compatibilidade.

## 3) Escopo e restricoes obrigatorias
- Nao implementar RBAC completo no MVP.
- Nao coletar dados individuais de alunos.
- Sem frontend proprio no MVP.
- Endpoints BI `v1` sao read-only.
- Seguir ordem de fases definida em `CODEX_TASKS.md`.

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

## 8) Riscos atuais
- `IMA` ainda existe e pode induzir leitura errada se continuar em destaque no BI.
- Comparacoes entre anos escolares diferentes exigem contexto de etapa/fonte.
- A migracao visual do dashboard do Metabase ainda precisa ser concluida no ambiente da instancia.

## 9) Proximos passos naturais
1. Concluir o dashboard do Metabase com foco em componentes.
2. Adicionar catalogo de metricas e dicionario de dados.
3. Evoluir governanca e qualidade de dados.
4. Planejar deploy de homologacao/producao.

## 10) Prompt base
```text
Voce esta apoiando a evolucao de uma plataforma municipal de inteligencia educacional.

Contexto:
- Stack: FastAPI + PostgreSQL + Metabase OSS.
- Hierarquia: Municipio -> Escola -> Turma -> Indicadores.
- Sem dados individuais de alunos.
- Base semantica atual:
  - CNCA para 1o-5o ano
  - MEC Anos Finais BNCC para 6o-9o ano
  - Saeb como referencia complementar
- Metricas principais:
  - percentual no esperado em leitura
  - percentual no esperado em escrita
  - percentual no esperado em matematica
- IMA e legado temporario.
- Endpoints BI principais: /bi/v1/indicadores-componentes e /bi/v1/desempenho.

Objetivo deste pedido:
[descreva aqui o tipo de insight que voce quer]

Restricoes:
- Nao quebrar contratos existentes sem estrategia de transicao.
- Nao adicionar dados individuais.
- Priorizar baixo custo operacional e simplicidade de manutencao.
```
