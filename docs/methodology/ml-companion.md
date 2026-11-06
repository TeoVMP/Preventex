# The machine-learning companion

- **Status:** rules document. The module does not exist yet.
- **Authority:** optional model. The deterministic model is the reference (ADR 0002).

## Role

The machine-learning model is a challenger, never the authority. It exists to be compared with the deterministic model: when they agree, confidence increases; when they diverge, we investigate. Preventex must run and display correctly without this module installed.

## Architecture

- A separate, pluggable module with the same interface as the deterministic model: same inputs (day, zone, features), same output shape (number, class, provenance).
- Off by default in the viewer. Every output is labelled with the model name and version.
- The core must not import it. Dependency direction: the companion depends on the core's data, never the reverse.

## Data rules

- Training data is versioned, with provenance and licence, in a documented dataset (source, period, processing).
- Labels come from official historical records where available: BDIFF (France) and the ICNF records (Portugal). Spain's EGIF is not open; for Spain we start with EFFIS burned-area perimeters (large fires only) and document the bias this introduces.
- Gaps and biases in labels are documented in the dataset card, not hidden.

## Training rules

- **Temporal splits only.** Train on earlier years, test on later years. Random shuffling is forbidden: it leaks the future into the past.
- Use block splits by season and region when evaluating, because fires cluster in time and space.
- Class imbalance is expected (extreme days are rare). Report precision, recall, PR-AUC and Brier score. Accuracy alone is forbidden.
- Every trained version records: code hash, dataset version, hyperparameters and results. Unreproducible models are not published.

## Publication rules

- Explainability (for example feature importance or SHAP values) is required before any output is published. If the model cannot show its reasoning, the output is not published.
- Extremes unlike the training data are out-of-distribution and are expected to fail. The deterministic model wins those days by design.
- Nonstationarity (climate shift) requires drift monitoring and recalibration, documented here when it happens.

## Agreement with the deterministic model

Measured, never eyeballed. The metrics are defined in `validation-plan.md`. Divergence is an anomaly signal: it is investigated and documented, not suppressed.

## Build order

Built after the deterministic pipeline has produced data (ADR 0002). Not before.
