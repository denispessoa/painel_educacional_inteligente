# ADR 008 – Learning Fact Table

## Status

Accepted

---

## Context

The system requires a flexible analytical structure to support educational dashboards.

The existing model stores indicators in aggregated form, limiting deeper analysis.

---

## Decision

Introduce a fact table named `fato_aprendizagem`.

Each record represents an aggregated learning measurement.

Structure:

- avaliacao_id
- turma_id
- componente
- dominio
- descritor
- valor

---

## Consequences

Benefits:

- supports domain-level analysis
- supports descriptor-level diagnostics
- improves Metabase queries
- maintains compatibility with existing indicators

---

## Impact

Low implementation complexity.

No breaking changes to the existing system.
