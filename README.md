# fire-platform (working name)

An open and auditable platform that collects public wildfire information for Spain, Portugal and France. It shows where the sources agree and where they do not.

**This is not an official alert system. Do not use it for emergency decisions. In an emergency, call 112.**

## Status

Early stage. Nothing is operational yet.

| Phase | Goal | Status |
|---|---|---|
| P0 | Core: API key handling, source documentation and tests | In progress |
| P1 | Satellite monitoring: NASA FIRMS, EFFIS, LSA SAF | Planned |
| P2 | Fire danger: AEMET, IPMA, Météo-France and the Fire Weather Index (FWI) | Planned |
| P3 | Comparison of sources and validation against historical records | Planned |
| P4 | Read-only viewer and API in Spanish, French, Portuguese and English | Planned |

Cameras are not part of v1. They will come later.

## Principles

- **Open.** The code is licensed under AGPL-3.0. Anyone can read, reuse and change it.
- **Transparent.** Every number shows its source, its time and the method used.
- **Deterministic.** The core has no AI. The same input gives the same output.
- **Respectful of data terms.** The licence, limits and attribution of each source are documented in `sources/` before the source is used.
- **No donations.** The project does not ask for donations. While it uses Fogos.pt data, it shows no funding requests of any kind. See [ADR 0001](docs/adr/0001-initial-decisions.md).

## Repository structure

| Folder | What is inside |
|---|---|
| `docs/` | Decisions (`docs/adr/`) and methods (`docs/methodology/`) |
| `sources/` | One folder per data source: licence, limits, update frequency and attribution. Connectors go here too, when they exist |
| `validation/` | Planned tests against historical fire records |
| `tests/` | Automated tests |
| `tools/` | Helper programs. The first one is `apikeys.py` |

The status of each data source is in [sources/README.md](sources/README.md).

## Quick start

You need Python 3.9 or newer. No third-party packages are required.

```bash
python3 tools/apikeys.py init                # create the local secrets file
python3 tools/apikeys.py set FIRMS_MAP_KEY   # paste a key; the input is hidden
python3 tools/apikeys.py check               # test the keys that are set
```

Keys are stored outside this repository, in `~/.config/fire-platform/secrets.env`. Never commit keys, tokens or passwords. More details in [tools/README.md](tools/README.md).

## Get involved

- **Students:** open an issue titled "Introduction" with your skills and your weekly hours. Look for issues labelled "good first issue". (Spanish: "Presentación".)
- **Researchers:** open an issue titled "Research contribution" to review the methods or the validation design. (Spanish: "Contribución investigadora".)
- **Translators:** the documentation is planned in English, Spanish, French and Portuguese. Only English exists so far.

## Data sources and attribution

Current attribution rules. Full details are in `sources/`.

- **LSA SAF (EUMETSAT):** cite "EUMETSAT LSA SAF" and the product name. Licence: CC BY 4.0.
- **AEMET:** cite AEMET as the author of the information.
- **Fogos.pt:** show "Fonte: Fogos.pt" with a link to https://fogos.pt next to the data. Its terms also forbid ads, donations, crowdfunding and other funding in services that use its data, and forbid using it as the only source in emergencies.

## Licence

GNU Affero General Public License v3.0 (AGPL-3.0). See [LICENSE](LICENSE).

## Contact

For now, use GitHub issues. A project email address will be added.

## Languages

This README is in English. Spanish, French and Portuguese versions are planned.
