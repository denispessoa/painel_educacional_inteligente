# System Context – Painel Educacional Inteligente

## Project Overview

This repository implements a **Municipal Educational Intelligence Platform** designed to monitor learning indicators across the municipal school network.

The system is used by the **Municipal Department of Education of Mendes (RJ, Brazil)**.

The platform provides dashboards and analytics for:

* school performance
* learning indicators
* literacy monitoring
* comparison with external assessments

The system operates using **aggregated data** and does not store individual student records.

---

# Technology Stack

Backend:

FastAPI
Python

Database:

PostgreSQL

Analytics:

Metabase

Development tools:

VS Code
Codex / AI-assisted development

---

# Core Data Model

The system follows this hierarchy:

Municipio
↓
Escola
↓
Turma
↓
Avaliacao
↓
Indicadores de aprendizagem

---

# Evaluation Model

Municipal evaluation is the **primary monitoring mechanism**.

External evaluations are integrated only for benchmarking.

Supported sources:

| source    | description                               |
| --------- | ----------------------------------------- |
| REDE      | municipal evaluation                      |
| CNCA      | Compromisso Nacional Criança Alfabetizada |
| SAEB      | national assessment                       |
| AVALIA_RJ | state-level evaluation                    |

---

# Educational Architecture

The system follows a pedagogical evaluation model structured as:

BNCC
↓
Municipal Curriculum (Mendes)
↓
Descriptor Progression Map
↓
Reference Matrix
↓
Evaluation Blueprint
↓
Municipal Assessments
↓
Aggregated Learning Indicators

---

# Evaluation Cycles

The system uses the concept of **ciclo_avaliativo**.

| cycle         | grades |
| ------------- | ------ |
| alfabetizacao | 1º–3º  |
| anos_iniciais | 4º–5º  |
| anos_finais   | 6º–9º  |

These cycles support pedagogical analysis and literacy monitoring.

---

# Learning Indicators

Indicators are stored in the analytical table:

fato_aprendizagem

Structure:

| field        | description            |
| ------------ | ---------------------- |
| avaliacao_id | evaluation reference   |
| turma_id     | class reference        |
| componente   | LP or MAT              |
| dominio      | pedagogical domain     |
| descritor    | descriptor code        |
| valor        | performance percentage |

---

# Pedagogical Domains

Portuguese:

* Consciência Fonológica
* Decodificação
* Fluência
* Compreensão
* Interpretação

Mathematics:

* Números
* Operações
* Álgebra
* Geometria
* Grandezas e Medidas
* Probabilidade e Estatística

---

# Analytical Layer

Metabase dashboards query data from the analytical view:

vw_desempenho_aprendizagem

This view aggregates learning indicators across:

* year
* trimester
* evaluation cycle
* component
* domain
* descriptor

---

# Architecture Decisions

Key architectural decisions are documented as ADRs in:

docs/architecture_decisions/

Important ADRs:

ADR_007 – Item Bank Deferred
ADR_008 – Learning Fact Table
ADR_009 – Evaluation Cycle Field
ADR_010 – Educational Semantic Layer
ADR_011 – Municipal Evaluation as Primary Source

---

# Development Guidelines

When modifying the system:

1. Do not remove existing tables
2. Prefer additive migrations
3. Maintain backward compatibility
4. Document architectural decisions
5. Keep pedagogical terminology in Portuguese
6. Keep system architecture documentation in English

---

# Future Roadmap

Planned improvements include:

* item bank module
* proficiency scale
* automatic pedagogical diagnostics
* geographic school analysis
* predictive analytics

These features will be implemented in later phases.

---

## AI Decision Context

Architectural decisions from the AI-assisted design phase are documented in:

`docs/AI_DECISION_CONTEXT.md`

Detailed decisions are stored as ADR files in:

`docs/architecture_decisions/`
