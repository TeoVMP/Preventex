# Validation plan (phase P3)

- **Status:** plan. Not started.

## Goals

1. Validate our deterministic computation against independent references.
2. Contrast data sources with each other (the platform's core idea).
3. Compare the deterministic model with the machine-learning companion, when it exists.

## Reference data

| Reference | Use | Status |
|---|---|---|
| EFFIS FWI | Compare our FWI computation | Available without key |
| Official national danger products (AEMET, IPMA, Météo-France) | Compare classes and thresholds | Pending per source |
| Historical fire records (BDIFF, ICNF, EFFIS burned area) | Validate danger and detections against real fires | Pending review |

Spain's EGIF is not open. Catalonia's Bombers response records are a candidate regional dataset for Spain, pending licence review.

## Metrics

**FWI against a reference** (per station, day, region and season):

- correlation and rank correlation;
- RMSE and bias;
- confusion matrix of danger classes.

**Detections and alerts against historical records:**

- precision and recall with explicit spatial and temporal tolerances, defined before running, not after;
- lead time;
- missed events and false alarms, reported separately by region and season.

**Deterministic against machine-learning:**

- rank correlation of daily danger by zone;
- confusion matrix of danger classes;
- Brier score where the machine-learning output is probabilistic.

## Protocol

- Periods, regions and tolerances are fixed and written down **before** looking at results (pre-registration), to avoid post-hoc choices.
- Results are published openly with data and code, including negative results.
- Known pitfalls, checked in review: temporal leakage, selection bias (large fires only), double counting (one fire, many satellite detections), tolerance calibration.

## Sequence

1. Pilot: FWI at Spanish weather stations, compared with EFFIS.
2. Extend to Portugal and France.
3. Detection contrast: FIRMS against LSA SAF against historical records.
4. Machine-learning comparison, when the module exists.
