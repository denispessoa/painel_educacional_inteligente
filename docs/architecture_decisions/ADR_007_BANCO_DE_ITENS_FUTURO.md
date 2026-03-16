# ADR 007 – Item Bank Deferred

## Status

Accepted

---

## Context

The municipal evaluation system could include an item bank for generating assessments.

However, implementing an item bank would require:

- item authoring workflows
- student-level data storage
- scoring engines
- psychometric calibration

These features are outside the scope of the current project phase.

---

## Decision

The system will NOT implement an item bank in the current phase.

Instead, it will operate with **aggregated learning indicators** generated from external evaluation processes.

---

## Consequences

Benefits:

- simpler architecture
- faster development
- lower operational complexity
- no storage of student-level data

Future possibility:

A modular item bank may be implemented later without impacting the current architecture.