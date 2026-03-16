# AI Decision Context – Educação Inteligente

This document summarizes architectural decisions discussed during the AI-assisted design phase of the system.

These decisions originated from design discussions and are formalized in ADR files.

## Purpose

Provide context for AI agents (Codex / Copilot / LLMs) to understand why the system architecture was designed this way.

---

# Key Architectural Decisions

The following ADRs represent the main design decisions:

ADR_007 – Item Bank Deferred  
ADR_008 – Learning Fact Table  
ADR_009 – Evaluation Cycle Field  
ADR_010 – Educational Semantic Layer  
ADR_011 – Municipal Evaluation as Primary Source

---

# Core Design Principles

1. The system operates on **aggregated educational indicators**.
2. Student-level data is intentionally **not stored**.
3. Municipal evaluations are the **primary monitoring mechanism**.
4. External evaluations are used only for **benchmarking**.
5. The analytical model is based on a **fact table architecture**.

---

# Analytical Data Model

The analytical model introduced the table:

`fato_aprendizagem`

Purpose:

Store learning indicators by:

- component
- domain
- descriptor

This table feeds the analytical view:

`vw_desempenho_aprendizagem`

Used by Metabase dashboards.

---

# Educational Architecture

The system follows this pedagogical flow:

BNCC  
↓  
Municipal Curriculum  
↓  
Descriptor Progression Map  
↓  
Reference Matrix  
↓  
Evaluation Blueprint  
↓  
Municipal Assessments  
↓  
Aggregated Indicators  
↓  
Metabase Dashboards

---

# Guidance for AI Agents

When modifying the system:

- follow the ADR decisions
- maintain backward compatibility
- do not remove existing tables
- prefer additive migrations

---

# Implementation Note

This file records the **official architectural direction** of the repository.

It should not be interpreted as proof that every structure is already fully implemented in the current runtime or database state.
