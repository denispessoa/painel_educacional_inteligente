# ADR 010 – Educational Semantic Layer

## Status

Accepted

---

## Context

Educational indicators require interpretation within a pedagogical framework.

Raw numerical indicators alone do not convey the meaning of learning outcomes.

For example:

| indicador | valor |
| --------- | ----- |
| leitura   | 45%   |

Without context, it is unclear what learning difficulty this represents.

To address this, the system introduces a **semantic layer** that maps indicators to pedagogical concepts.

---

## Decision

Create a **semantic layer** describing the educational meaning of indicators.

The semantic layer will be stored as reference files within the repository.

Examples of semantic datasets:

* componentes_curriculares.csv
* fases_ensino.csv
* fontes_avaliacao.csv
* indicadores_educacionais.csv

These files define the pedagogical interpretation of analytical data.

---

## Consequences

Benefits:

* separates data storage from pedagogical meaning
* improves dashboard interpretation
* allows AI-assisted diagnostic explanations
* facilitates alignment with curriculum structures

Example mapping:

| indicador | dominio             |
| --------- | ------------------- |
| leitura   | compreensão textual |

This mapping enables automated pedagogical explanations.

---

## Impact

No database schema changes required.

The semantic layer exists as documentation and reference datasets.
