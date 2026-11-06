# Fire Weather Index (FWI)

- **Status:** first documentation. Not implemented yet. Pilot planned for Spain.
- **Model:** deterministic (ADR 0002, reference model).

## What it is

The Fire Weather Index estimates the danger of a wildfire from weather alone. It was developed in Canada (van Wagner, 1987) and is the international standard: EFFIS uses it at European scale, and AEMET, IPMA and Météo-France (as IFM, its French adaptation) use it or adapt it.

Two properties make it the right backbone for Preventex:

- **It is deterministic.** Same inputs, same output, every time. Every number can be traced to equations and to input data.
- **It has memory.** Each day's value is computed from the previous day's state plus today's weather. One rainy day does not erase a two-month drought.

## Inputs

Daily weather, ideally observed around solar noon:

| Input | Unit |
|---|---|
| Temperature | °C |
| Relative humidity | % |
| Wind speed (10 m) | km/h |
| Precipitation (previous 24 h) | mm |

How each of our data sources provides these values (station observations, model output, noon extraction) is documented per source in `sources/`.

## Components

The system is a chain of simple, documented equations.

**Fuel moisture codes** (state carried from day to day):

| Code | Represents | Response time |
|---|---|---|
| FFMC | Fine fuels: litter, twigs | Hours (about 1 day) |
| DMC | Loosely compacted organic layer | About 12 days |
| DC | Deep, compact organic layer | About 52 days (seasonal) |

**Behaviour indices** (computed each day):

| Index | Meaning |
|---|---|
| ISI | Initial spread rate (FFMC + wind) |
| BUI | Fuel available to burn (DMC + DC) |
| FWI | Potential intensity (ISI + BUI) |

Values are unitless and open-ended. They are grouped into danger classes (for example the six EFFIS classes, from "very low" to "extreme") with **regional thresholds**: the same FWI number does not mean the same danger in Galicia and in Almería.

**Pending:** exact class thresholds per region, with official citations, will be added here. We do not invent thresholds.

## Season start and carry-over

The moisture codes start from fixed values at the beginning of the fire season. Overwintering (carrying DC and DMC across the winter, with adjustments) is supported by the standard; our policy will be documented here before implementation.

## Implementation

We use **xclim** (BSD-3-Clause, licence-compatible with AGPL-3.0), which implements the FWI system (`xclim.indices.fire`), including the moisture codes, the indices and fire-season handling. We do not re-implement the equations ourselves; we validate the implementation against reference data.

References:

- van Wagner, C.E. (1987). *Development and structure of the Canadian Forest Fire Weather Index System*. Canadian Forestry Service, Technical Report 35.
- Lawson, B.D. & Armitage, O.B. (2008). *Weather guide for the Canadian Forest Fire Danger Rating System*. Natural Resources Canada.

## Data sources for the pilot (Spain)

| Source | Use | Status |
|---|---|---|
| AEMET OpenData | Station weather | Key working |
| EFFIS | FWI reference maps for validation | Available without key |
| Open-Meteo | Provisional fallback if AEMET data has gaps | Documented as non-official |

Portugal follows with IPMA (no key needed). France waits for Météo-France access; until then Open-Meteo is a documented, non-official substitute.

## Known limits

- The FWI was calibrated for Canadian fuel types. European vegetation differs; regional thresholds and interpretation carry that burden.
- It does not know the state of the vegetation (for example shrub dryness via NDVI), the terrain, or the fire history of a site.
- It does not predict ignitions. See `prediction-scope.md`.
- Noon-weather gaps must be handled with a documented policy: gap filling is a method choice, not a detail.

## Validation

Our computed FWI will be compared with EFFIS and with official national products, following `validation-plan.md`.
