# Plano de Implantacao das Fases Pos-MVP

Plano de implantacao para as fases 5-8, com foco em previsibilidade, baixo risco e continuidade operacional.

## Principios
- Implantacao incremental por ondas.
- Compatibilidade retroativa dos contratos publicos.
- Controle por gates de qualidade antes de promover ambiente.
- Rollback claro para cada release.

## Ambientes e objetivos
- `dev`: desenvolvimento e validacao tecnica diaria.
- `hml`: homologacao funcional com validacao de negocio e BI.
- `prod`: uso operacional oficial.

## Estrategia por onda

## Onda 1 - Base operacional (Fase 5)
- Implantar CI/CD, observabilidade minima e runbooks.
- Gate para avancar:
  - testes automatizados verdes
  - deploy de homologacao automatizado
  - validacao de restore de backup

## Onda 2 - Governanca de dados (Fase 6)
- Implantar dicionario de dados, metricas e checks de qualidade.
- Gate para avancar:
  - conformidade das metricas no BI
  - validacao de contratos `v1`
  - monitoramento de qualidade de dados ativo

## Onda 3 - Seguranca incremental (Fase 7)
- Implantar autenticacao e RBAC por etapas.
- Gate para avancar:
  - matriz de permissao validada
  - auditoria de eventos sensiveis
  - smoke tests de seguranca aprovados

## Onda 4 - Expansao de produto (Fase 8)
- Implantar modulos de evolucao de produto com rollout controlado.
- Gate para avancar:
  - telemetria funcional ativa
  - indicadores de adocao definidos
  - plano de suporte operacional ajustado

## Plano tecnico de release

## Checklist pre-release
- Suite de testes backend (`pytest`) 100% verde.
- Smoke test dos endpoints:
  - `/health`
  - `/analytics/ima`
  - `/bi/v1/hierarquia`
  - `/bi/v1/indicadores-trimestrais`
  - `/bi/v1/ima`
- Validacao de migracoes/DDL (quando houver).
- Atualizacao de documentacao operacional e de contrato.

## Checklist pos-release
- Health da API e conectividade com banco.
- Validacao de consultas BI em homologacao/producao.
- Monitoramento de erros HTTP 5xx e latencia.
- Confirmacao de backup agendado e logs ativos.

## Rollback
- API:
  - rollback de versao por artefato da release anterior.
- Banco:
  - se houver mudanca de schema, rollback com plano definido no release.
- BI:
  - manter contrato anterior ativo ate estabilizacao.

## Responsabilidades (RACI simplificado)
- Engenharia backend: implementacao, testes, deploy tecnico.
- Responsavel BI: validacao de consumo e semantica.
- Produto/gestao: aprovacao de aceite funcional.
- Operacao: monitoramento e resposta a incidentes.

## Indicadores de sucesso da implantacao
- Taxa de sucesso de deploy.
- Tempo medio de recuperacao (MTTR).
- Erros 5xx apos release.
- Tempo de atualizacao dos dashboards BI.

## Cronograma sugerido (referencia)
- Ciclo 1 (2-4 semanas): Fase 5.
- Ciclo 2 (2-4 semanas): Fase 6.
- Ciclo 3 (3-5 semanas): Fase 7.
- Ciclo 4 (4-8 semanas): Fase 8.

## Dependencias criticas
- Ambiente de homologacao estavel.
- Monitoramento minimo configurado.
- Disponibilidade de validacao funcional/BI em cada onda.
