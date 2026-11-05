# tools/apikeys.py

A small terminal helper to store API keys safely, check that they work, and get short-lived OAuth2 tokens where a provider supports it.

## Quick start

```bash
python3 tools/apikeys.py init                # create the local secrets file
python3 tools/apikeys.py set FIRMS_MAP_KEY   # paste the key; the input is hidden
python3 tools/apikeys.py list                # keys are masked; sign-up pages are listed
python3 tools/apikeys.py check               # tests every key that is set
```

## Commands

| Command | What it does |
|---|---|
| `init` | Creates the secrets file. It never overwrites an existing file. |
| `list` | Shows which keys are set (masked) and where to get each one. |
| `set NAME` | Stores a key. Use `--stdin` to pass the value from another command. |
| `unset NAME` | Removes a key. |
| `check [PROVIDER]` | Makes one read-only request per provider to test its key. |
| `login meteofrance` | Gets an OAuth2 token and shows when it expires. The token is not printed. |
| `token meteofrance` | Prints a token to standard output. Only for pipelines. |
| `doctor` | Checks file permissions and whether git could commit the secrets file. |

## Where keys live

- Default file: `~/.config/fire-platform/secrets.env`. The folder is readable only by you (700) and the file too (600).
- To use another path, set `FIRE_PLATFORM_SECRETS=/path/to/file.env`.
- Environment variables with the same names override the file. This is how continuous integration (GitHub Actions secrets) uses them.
- Never paste keys into chats, issues, screenshots or logs. If a key leaks, revoke it on the provider's site and create a new one.

## What it does not do, on purpose

- It does not log in to provider websites with your username and password. That usually breaks the provider's terms of use, often needs CAPTCHAs or email confirmation, and would mean storing passwords.
- It does not create accounts or request keys for you. Each key is created on the provider's site, using the project email address.

## Requirements

Python 3.9 or newer. No third-party packages.

## Status

Version 0.1.0. Translations into Spanish, French and Portuguese will follow the project's documentation process.
