# Educational Data Architecture – Painel Educacional Inteligente

## Overview

This document describes the educational data architecture used in the **Painel Educacional Inteligente** project.

The system supports a **Municipal Educational Intelligence Platform** designed to:

- Monitor learning indicators
- Integrate municipal and external evaluations
- Provide pedagogical diagnostics
- Support educational decision-making

The system uses **aggregated data** and does not store individual student records.

---

# Core Principles

The architecture follows these principles:

1. Municipal evaluation is the main monitoring tool
2. External evaluations serve as benchmarks
3. Alignment with BNCC
4. Aggregated indicators instead of student-level data
5. Clear separation between pedagogy and analytics

---

# Educational Evaluation Flow

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
Aggregated Learning Results  
↓  
fato_aprendizagem  
↓  
Metabase Dashboard  
↓  
Pedagogical Diagnostics  

---

# Pedagogical Structure

## Components

LP – Língua Portuguesa  
MAT – Matemática

---

## Portuguese Domains

- Consciência Fonológica
- Decodificação
- Fluência
- Compreensão
- Interpretação

---

## Mathematics Domains

- Números
- Operações
- Álgebra
- Geometria
- Grandezas e Medidas
- Probabilidade e Estatística

---

# Evaluation Cycles

The system introduces the concept of **ciclo_avaliativo**.

| Cycle | Grades | Description |
|------|------|------|
| alfabetizacao | 1º–3º | literacy development |
| anos_iniciais | 4º–5º | competency consolidation |
| anos_finais | 6º–9º | preparation for SAEB |

---

# Evaluation Sources

| Source | Description |
|------|------|
| REDE | municipal evaluation |
| CNCA | national literacy evaluation |
| SAEB | national assessment |
| AVALIA_RJ | state evaluation |

Municipal evaluation remains the **primary monitoring mechanism**.

---

# Database Architecture

Core tables:

municipios  
escolas  
turmas  
avaliacoes  
fato_aprendizagem  

---

# Fact Table – Learning Indicators

Table: `fato_aprendizagem`

| Field | Description |
|------|------|
| id | primary key |
| avaliacao_id | evaluation reference |
| turma_id | class reference |
| componente | LP or MAT |
| dominio | pedagogical domain |
| descritor | descriptor code |
| valor | performance percentage |

---

# Analytical View

The main analytical view used by Metabase:

`vw_desempenho_aprendizagem`

This view aggregates performance by:

- year
- trimester
- evaluation cycle
- school grade
- component
- domain
- descriptor

---

# Pedagogical Diagnostic Layer

The system supports automatic interpretation of learning indicators.

Example:

Indicator: interpretação textual = 45%

Diagnosis:  
Students show difficulty inferring information from texts.

Suggested intervention:  
Activities focused on textual inference.

---

# Future Roadmap

Planned improvements:

- Item bank
- Proficiency scale
- Geographic analysis of schools
- Predictive learning analytics
- Automated pedagogical diagnostics

---

# Benefits

This architecture enables:

- scalable analytics
- pedagogical clarity
- compatibility with BNCC and SAEB
- advanced dashboards
- sustainable system evolution
