# Essencia do Projeto (Contexto para IA)

Use este arquivo como contexto base para pedir insights tecnicos, de produto e de operacao em outras IAs.

## 1) Resumo executivo
- Projeto: Plataforma Municipal de Inteligencia Educacional (MVP).
- Objetivo: apoiar gestao educacional municipal com dados agregados de alfabetizacao.
- Regra central: sem dados individuais de alunos.
- Stack principal: FastAPI + PostgreSQL + Metabase OSS (Power BI em transicao).
- Hierarquia de dados: `Municipio -> Escola -> Turma -> Indicadores`.

## 2) Problema que o projeto resolve
- Consolidar dados educacionais por territorio e unidade escolar.
- Permitir acompanhamento trimestral de leitura/escrita por turma.
- Entregar dados confiaveis para consumo analitico no Metabase/Power BI.

## 3) Escopo e restricoes obrigatorias
- Nao implementar RBAC completo no MVP.
- Nao coletar dados individuais de alunos.
- Sem frontend proprio no MVP.
- Endpoints BI `v1` sao read-only e com contrato estavel.
- Seguir ordem de fases definida em `CODEX_TASKS.md`.

## 4) O que ja foi entregue
- Fase 1: CRUD de `municipios`, `escolas`, `turmas`.
- Fase 2: `indicadores-trimestrais` (contagens + percentuais calculados no backend).
- Fase 3: endpoint de analytics IMA (`/analytics/ima`).
- Fase 4: endpoints BI read-only em `/bi/v1/*`.
- Fase 5 (inicio): baseline operacional:
  - CI backend
  - observabilidade minima (`/metrics`, `/health/dependencies`, logs JSON)
  - scripts de backup/restore
  - runbook de incidentes
- Fase 5.1: migracao de BI para Metabase OSS em paralelo ao Power BI.

## 5) Modelo de dados (visao curta)
- Entidades: `Municipio`, `Escola`, `Turma`, `IndicadorTrimestral`.
- Regras-chave:
  - `estado` com 2 letras (normalizado para maiusculo).
  - FKs obrigatorias entre hierarquia.
  - Unicidade em indicadores por `turma_id + ano + trimestre`.
  - Sem cascade em deletes com dependencia (bloqueio por integridade).
- IMA (agregado): media operacional de leitura e escrita; base pedagogica oficial registrada em `docs/IMA_REFERENCE_BASE.md`.

## 6) Contratos de API (visao curta)
- CRUD base:
  - `/municipios`
  - `/escolas`
  - `/turmas`
  - `/indicadores-trimestrais`
- Analytics:
  - `GET /analytics/ima`
- BI v1:
  - `GET /bi/v1/hierarquia`
  - `GET /bi/v1/indicadores-trimestrais`
  - `GET /bi/v1/ima`
- Contrato de erros:
  - `422` validacao
  - `404` nao encontrado (CRUD)
  - `409` conflito de integridade (CRUD)
  - BI v1: foco em `200/422` para consumo analitico

## 7) Estado operacional atual
- Testes backend: passando (`43 passed`).
- API com health basico e health de dependencia.
- CI de backend configurado em GitHub Actions.
- Banco local em Docker Compose.
- Metabase OSS local configurado para camada BI em transicao.
- Power BI mantido como legado temporario/rollback.

## 8) Pendencias e proximas fases
- Fase 5 (continuacao): pipeline de deploy para homologacao/producao + alertas.
- Fase 6: governanca de dados e BI (dicionario de dados, catalogo de metricas, qualidade).
- Fase 7: seguranca incremental (autenticacao + RBAC por etapas).
- Fase 8: evolucao de produto.
- Decisao registrada: reduzir custo de BI com Metabase OSS ate haver faturamento.

## 9) Riscos atuais
- Operacao paralela Metabase/Power BI exige disciplina de paridade de dashboard.
- Ainda sem deploy automatizado completo.
- Sem monitoramento externo de disponibilidade.

## 10) Perguntas prontas para pedir insights em outra IA
1. "Com base neste contexto, proponha um plano tecnico de deploy em homologacao/producao para FastAPI + PostgreSQL com rollback."
2. "Sugira um pacote minimo de observabilidade e alertas para a Fase 5 com baixo custo operacional."
3. "Proponha um dicionario de dados e catalogo de metricas para a Fase 6 sem quebrar o contrato BI v1."
4. "Quais testes de qualidade de dados devo adicionar para garantir consistencia dos indicadores trimestrais e IMA?"
5. "Desenhe uma estrategia incremental de autenticacao/RBAC para a Fase 7 sem impacto em consumidores BI."

## 11) Prompt base (copiar e colar)
```text
Voce esta apoiando a evolucao de uma plataforma municipal de inteligencia educacional.

Contexto:
- Stack: FastAPI + PostgreSQL + Metabase OSS.
- Hierarquia: Municipio -> Escola -> Turma -> Indicadores.
- Sem dados individuais de alunos.
- Sem RBAC completo no MVP.
- Fases concluidas: 1 a 4.
- Fase 5 iniciada com CI, observabilidade minima e backup/restore.
- Fase 5.1 em andamento com migracao BI para Metabase.
- Contratos BI v1 read-only ja publicados em /bi/v1/*.

Objetivo deste pedido:
[descreva aqui o tipo de insight que voce quer]

Restricoes:
- Nao quebrar contratos existentes.
- Nao adicionar dados individuais.
- Priorizar baixo custo operacional e simplicidade de manutencao.

Entregue:
- plano pratico por etapas
- riscos e mitigacoes
- criterio de aceite tecnico
- exemplos concretos de implementacao
```
