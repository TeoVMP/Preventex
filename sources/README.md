# Data sources

Each source gets its own folder here, for example `sources/firms/`. The folder holds the licence, the access method, the limits, the update frequency and the attribution. When the connector exists, it goes in the same folder.

This page summarises the status of each source. "Verified" means the licence or terms were read in the official source. "Pending review" means they have not been checked yet.

| Source | Used for | Access | Licence and attribution | Limits | Update | Status |
|---|---|---|---|---|---|---|
| NASA FIRMS | Active fire detections (satellite) | Free MAP_KEY from firms.modaps.eosdis.nasa.gov/api/map_key | Pending review | 5,000 transactions per 10 minutes per key | Pending review | Partly verified |
| LSA SAF FRP-PIXEL (EUMETSAT) | Fire radiative power per pixel, from MSG and MSG-IODC | Free registration; HTTP at datalsasaf.lsasvcs.ipma.pt | CC BY 4.0. Cite "EUMETSAT LSA SAF" and the product | Archive restricted to registered users | Every 15 minutes | Verified |
| AEMET OpenData | Observations and forecasts (Spain) | Free API key requested on the AEMET OpenData site | Cite AEMET as the author of the information | 40 requests per minute per user; HTTP 429 when exceeded. New keys expire after 3 months | Pending review | Partly verified |
| Météo-France public APIs | Warnings, observations and forest weather (France) | Free account; subscribe to each API; OAuth2 credentials | Pending review | Set per API (Vigilance: about 60 requests per minute) | Pending review | Partly verified |
| Fogos.pt API | Incident information (Portugal) | Access request form; header `X-API-Key` | Show "Fonte: Fogos.pt" with a link. No ads, donations, crowdfunding or other funding in services that use it | Set by Fogos.pt; not yet published | Pending review | Terms verified |
| IPMA API | Forecasts and warnings (Portugal) | Public (api.ipma.pt) | Pending review | Pending review | Pending review | Not verified |
| EFFIS / GWIS | Fire danger (FWI) and burnt areas | Public services | Pending review | Pending review | Pending review | Not verified |
| Copernicus Climate Data Store (ERA5) | Historical weather for validation | Free account; API token | Pending review (licence set per dataset) | Pending review | Pending review | Not verified |
| BDIFF (France, 2006–2022) | Historical fire records for validation | data.gouv.fr | Pending review | Not applicable | Not applicable | Not verified |
