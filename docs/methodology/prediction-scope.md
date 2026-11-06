# Prediction scope: what we predict and what we do not

- **Status:** first documentation.
- **Applies to:** all models, deterministic and machine-learning.

## The one-sentence version

We predict how flammable the landscape is, not where or when a fire will start.

## What we predict

- **Fire-danger conditions** (FWI components and danger classes) for today and for the following days (up to D+7) when forecast data allows, computed deterministically from observed and forecast weather.
- **Context statistics**: how unusual today's danger is compared with the same place and date in the historical record (percentiles), and seasonal outlooks.

## What we do not predict

- **Ignitions.** A fire needs an ignition source, and in Spain and Portugal official statistics attribute the large majority of ignitions to human causes. Weather cannot forecast human behaviour. The machine-learning companion may later estimate ignition probability per day and zone, always labelled as a statistical estimate and benchmarked against the deterministic reference.
- **Fire spread or perimeters.** Simulation of an ongoing fire is a later phase, if ever.
- **Emergency alerts.** Never. Preventex is not an alert system and does not replace 112 or the civil protection services.

## Conditional language rule

Danger is conditional: "IF an ignition happens, conditions favour rapid spread." All published text must use conditional phrasing ("conditions for", "favours"), never "will burn" or "fire expected here".

## Why this scope

- **Honesty:** the methods only support these claims.
- **Safety:** unmerited certainty in emergencies is harmful.
- **Legal and ethical:** we are not an official source (see the disclaimer in the README).
