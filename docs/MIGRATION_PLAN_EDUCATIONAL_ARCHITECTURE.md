# Migration Plan – Educational Data Architecture

## Objective

Introduce the new educational analytics architecture without breaking the existing system.

The migration follows a **non-breaking strategy**, adding new structures while keeping the current indicators operational.

---

# Migration Steps

## Step 1 – Documentation

Add architecture documentation:

- EDUCATIONAL_DATA_ARCHITECTURE.md
- Migration plan
- ADR decision records

---

## Step 2 – Database Change

Add field `ciclo_avaliativo` to the table `avaliacoes`.

Possible values:

- alfabetizacao
- anos_iniciais
- anos_finais

SQL:

ALTER TABLE avaliacoes
ADD COLUMN ciclo_avaliativo VARCHAR(30);

---

## Step 3 – Create Analytical Table

Create table `fato_aprendizagem`.

Purpose:

Store aggregated learning indicators by component, domain and descriptor.

---

## Step 4 – Create Analytical View

Create view:

vw_desempenho_aprendizagem

Used by Metabase dashboards.

---

## Step 5 – Validation

Validate:

- migrations run successfully
- current endpoints still work
- dashboards continue to operate
- analytical queries return data

---

# Backward Compatibility

The migration does not remove any existing table or column.

Existing dashboards continue using current indicators.

New dashboards can use the analytical model.
