# ADR 0002: Two prediction models — deterministic core and optional ML companion

- **Status:** accepted
- **Date:** 2026-11-06

## Context

Fire-danger prediction has two method families: deterministic formulations derived from physics (for example the Fire Weather Index) and statistical learning from historical records. They fail in different ways. The deterministic model is explainable and stable, but rests on assumptions calibrated elsewhere. A learning model can capture local patterns, but fails on events unlike its training data and cannot fully show its reasoning.

Comparing both families gives confidence when they agree and flags anomalies when they diverge. ADR 0001 forbids AI in the core. This record defines that boundary and the role of the machine-learning module.

## Decision

1. The deterministic model is the authoritative reference. The viewer shows it by default.
2. The machine-learning model is an optional companion: a separate, pluggable module with the same interface, never a dependency of the core, clearly labelled, and off by default. Every published number states which model produced it.
3. Rules for the machine-learning module:
   - temporal train/test splits, never random shuffles;
   - explainability is required before any output is published;
   - training data and models are versioned and reproducible;
   - agreement with the deterministic model is measured with defined metrics, not by eye;
   - divergence is treated as an anomaly signal, not as a failure.
4. Pilot: Spain first, with AEMET station data, validated against EFFIS.
5. The machine-learning module is built after the deterministic pipeline has produced data.

## Consequences

- ADR 0001 decision 3 (no AI in the core) remains in force; the machine-learning module lives outside the core.
- `docs/methodology/` documents both models, starting with `fwi.md`, `prediction-scope.md`, `ml-companion.md` and `validation-plan.md`.
- The viewer must be able to run and display the deterministic model without the machine-learning module installed.
- Adding the machine-learning module must not change the licence of the core: both remain AGPL-3.0.
