# ADR 0001: Initial decisions

- **Status:** accepted, except the open questions at the end.
- **Date:** 2026-11-05

## Context

The project shows public wildfire information for Spain, Portugal and France. Its sources and methods must be open to audit. A few early choices shape the whole project, so this record keeps them in one place.

## Decisions

1. **Licence: AGPL-3.0.** The code stays open, including when the project runs as a network service. Anyone can check how the numbers are produced.
2. **Scope of v1: data only.** v1 covers phases P0 to P4 (see the README). Cameras come later.
3. **No AI in the core.** Calculations use documented, deterministic methods, described in `docs/methodology/`.
4. **Every number has a source, a time and a method.**
5. **Official incident records are not a v1 dependency.** v1 uses satellite, weather, fire-danger and historical data.
6. **Fogos.pt data.** Use it only after access is granted through its request form, with an individual token sent in the `X-API-Key` header. Show "Fonte: Fogos.pt" with a link. Do not show ads, donation requests, crowdfunding or other funding requests in services that use its data. Do not use it as the only source for emergency decisions. Source: Fogos.pt API terms, sections 3, 4 and 9.
7. **No automated website logins.** The tools store and check API keys. They do not log in to provider websites with a username and password. Providers' terms usually forbid it, and it would mean storing passwords.
8. **No credentials in the repository.** Keys live in a local file outside the repository.

## Open questions

- **Legal host for funding.** Not decided. Options: an existing non-profit association, or a fiscal host.
- **Attribution clause (AGPL section 7(b)).** Not decided.
- **Name, project email and GitHub organisation.** Not decided. "fire-platform" is a working name.

## Consequences

- No data source is used before its licence, limits and attribution are documented in `sources/`.
- While Fogos.pt data is used, the platform shows no funding requests.
