# ADR 009 – Evaluation Cycle Field (ciclo_avaliativo)

## Status

Accepted

---

## Context

The municipal education analytics platform requires a way to organize evaluation results according to pedagogical learning stages.

The Brazilian educational system organizes monitoring by learning cycles rather than only by grade.

Examples include:

* Literacy cycle (early grades)
* Consolidation cycle (upper primary)
* Lower secondary cycle

Without an explicit cycle field, it becomes difficult to perform pedagogical analysis in dashboards.

---

## Decision

Introduce a field named **ciclo_avaliativo** in the table **avaliacoes**.

This field represents the pedagogical learning cycle associated with the evaluation.

Possible values:

* alfabetizacao (1º–3º ano)
* anos_iniciais (4º–5º ano)
* anos_finais (6º–9º ano)

---

## Consequences

Benefits:

* enables analysis by pedagogical stage
* aligns the system with BNCC and national policies
* improves literacy monitoring
* simplifies dashboard aggregation

Example analysis enabled by this field:

| ciclo_avaliativo | leitura |
| ---------------- | ------- |
| alfabetizacao    | 55%     |
| anos_iniciais    | 62%     |
| anos_finais      | 58%     |

---

## Impact

Low implementation complexity.

Requires a single additional column in the **avaliacoes** table.

No breaking changes to existing data structures.
