# ADR 011 – Municipal Evaluation as Primary Monitoring Source

## Status

Accepted

---

## Context

Many educational dashboards rely exclusively on external assessments such as SAEB or state-level evaluations.

However, these assessments are infrequent and cannot support continuous pedagogical monitoring.

For a municipal intelligence system, regular internal evaluation is required.

External assessments should be used as benchmarks rather than the primary monitoring mechanism.

---

## Decision

Define **municipal evaluations** as the primary source of learning indicators.

External evaluations will be integrated only as comparison layers.

Evaluation sources supported by the system include:

| source    | description                     |
| --------- | ------------------------------- |
| REDE      | municipal evaluation            |
| CNCA      | national literacy evaluation    |
| SAEB      | national large-scale assessment |
| AVALIA_RJ | state-level evaluation          |

---

## Consequences

Benefits:

* enables continuous monitoring
* improves intervention speed
* preserves compatibility with national assessments
* strengthens municipal autonomy

Example dashboard comparison:

| source | leitura |
| ------ | ------- |
| REDE   | 62%     |
| CNCA   | 58%     |
| SAEB   | 50%     |

---

## Impact

No structural database changes required.

Requires storing the **fonte_avaliacao** attribute in evaluation records.
