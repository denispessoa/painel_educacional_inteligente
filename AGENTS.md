# AI Agent Instructions – Painel Educacional Inteligente

This repository implements a Municipal Educational Intelligence Platform.

## Core Architecture

Official architectural baseline:

Municipio → Escola → Turma → Avaliacao → Indicadores

Current operational MVP:

Municipio → Escola → Turma → Indicadores

Analytical pipeline baseline:

Avaliacoes da Rede Municipal → Resultados agregados de aprendizagem → fato_aprendizagem → vw_desempenho_aprendizagem

The system uses aggregated educational indicators and does NOT store student-level data.

## Database

PostgreSQL

Current active tables:

municipios
escolas
turmas
indicadores_trimestrais
fato_aprendizagem

Architectural baseline and additive evolution:

avaliacoes
ciclo_avaliativo
escala de proficiencia
banco de itens

## Analytical Model

Indicators follow this hierarchy:

descritor → dominio → componente

Components:

LP – Língua Portuguesa
MAT – Matemática

## Deferred Concepts

These remain part of the pedagogical roadmap, but are not in the active migration batch:

alfabetizacao (1º–3º)
anos_iniciais (4º–5º)
anos_finais (6º–9º)

## Dashboard

Metabase queries data from analytical views.

Main view:

vw_desempenho_aprendizagem

## Architectural Decisions

AI agents must follow the architectural decisions documented in:

docs/AI_DECISION_CONTEXT.md  
docs/architecture_decisions/

## Rules for AI Agents

Do not delete existing tables.
Prefer additive migrations.
Maintain backward compatibility.
Always document migrations.
