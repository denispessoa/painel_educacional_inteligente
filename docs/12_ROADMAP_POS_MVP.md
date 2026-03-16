# Roadmap Pos-MVP (Fases 5-8)

Planejamento das fases seguintes apos a conclusao do MVP (Fases 1-4).

## Contexto atual
- Fase 1: CRUD da hierarquia municipal concluido.
- Fase 2: indicadores trimestrais concluido.
- Fase 3: analytics IMA concluido.
- Fase 4: endpoints read-only para Power BI concluido.

Restricoes mantidas:
- sem dados individuais de alunos
- sem RBAC completo no MVP (evolui apenas no pos-MVP)

## Fase 5 - Consolidacao Operacional

## Objetivo
Tornar o produto operavel com padrao minimo de confiabilidade para uso continuo.

## Entregaveis
- Pipeline CI (testes automatizados + checks de qualidade).
- Pipeline de deploy (ambiente de homologacao e producao).
- Runbook de incidentes (API, banco, BI).
- Politica de backup/restore validada.
- Observabilidade minima:
  - logs estruturados
  - metricas basicas de API
  - health checks de dependencia

## Criterios de aceite
- Deploy automatizado reproduzivel.
- RTO/RPO documentados e testados em simulacao.
- Alertas basicos funcionando para indisponibilidade da API.

## Fase 6 - Governanca de Dados e BI

## Objetivo
Padronizar semantica de dados e confiabilidade das metricas no consumo BI.

## Entregaveis
- Dicionario de dados oficial (campos, tipos, regras de negocio).
- Catalogo de metricas (definicoes de alfabetizacao e IMA).
- Contratos de versao para endpoints BI (`v1`, politica de breaking change).
- Testes de qualidade de dados para endpoints `/bi/v1/*`.
- Camada semantica no Power BI (modelo estrela, medidas padrao).

## Criterios de aceite
- Indicadores no BI com definicao unica e auditavel.
- Validacoes automatizadas para consistencia de percentuais e IMA.

## Fase 7 - Seguranca e Controle de Acesso (Pos-MVP)

## Objetivo
Introduzir autenticacao e autorizacao de forma incremental sem quebrar contratos de dados.

## Entregaveis
- Autenticacao de usuarios (provedor e fluxo definidos).
- RBAC incremental:
  - perfis administrativos
  - perfis operacionais
  - perfil leitura BI
- Auditoria minima de acoes sensiveis.
- Hardening de API:
  - rate limiting
  - CORS/headers de seguranca
  - gestao de secrets por ambiente

## Criterios de aceite
- Endpoints protegidos por perfil.
- Trilhas de auditoria para alteracoes de dados.
- Sem regressao no consumo BI read-only.

## Fase 8 - Evolucao de Produto

## Objetivo
Expandir valor de produto alem do MVP sem comprometer governanca.

## Entregaveis
- Dashboard proprio (complementar ao Power BI).
- Modulos analiticos adicionais (ex.: risco pedagogico em agregados).
- Melhorias de UX operacional para gestao municipal.
- Estrategia de integracao com sistemas externos.

## Criterios de aceite
- Novas features com telemetria e metricas de adocao.
- Roadmap de produto revisado trimestralmente.

## Ordem recomendada
1. Fase 5 (operacao)
2. Fase 6 (governanca de dados)
3. Fase 7 (seguranca e acesso)
4. Fase 8 (expansao de produto)

## Nao fazer neste ciclo (ainda)
- Dados individuais de alunos.
- Funcionalidades fora da hierarquia municipal estabelecida.
- Quebra de contrato dos endpoints BI `v1`.
