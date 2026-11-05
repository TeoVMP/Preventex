#!/usr/bin/env python3
"""apikeys: store, check and use API keys from the terminal.

Commands:
  init               Create the local secrets file. Never overwrites an existing file.
  list               Show which keys are set. Values are masked.
  set NAME           Store a key. Input is hidden. Use --stdin inside scripts.
  unset NAME         Remove a key.
  check [PROVIDER]   Check keys with one read-only request. Default: all.
  login meteofrance  Get an OAuth2 token and show when it expires. The token is not printed.
  token meteofrance  Print a fresh token to stdout. Only for use inside a pipeline.
  doctor             Check file permissions and git safety.

Not supported on purpose:
  Logging in to a provider's website with your password. That usually breaks the
  provider's terms of use, often needs CAPTCHAs or email confirmation, and forces
  you to store passwords. Create and renew keys on each provider's site yourself.

Requires Python 3.9 or newer. Standard library only.
"""

from __future__ import annotations

import argparse
import base64
import getpass
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

VERSION = "0.1.0"
TIMEOUT_SECONDS = 20

SECRETS_FILE = Path(
    os.environ.get("FIRE_PLATFORM_SECRETS")
    or Path.home() / ".config" / "fire-platform" / "secrets.env"
)
CDS_FILE = Path.home() / ".cdsapirc"

VARIABLES = {
    "FIRMS_MAP_KEY": ("firms", "NASA FIRMS MAP_KEY"),
    "AEMET_API_KEY": ("aemet", "AEMET OpenData API key"),
    "METEOFRANCE_CONSUMER_KEY": ("meteofrance", "Météo-France consumer key (OAuth2)"),
    "METEOFRANCE_CONSUMER_SECRET": ("meteofrance", "Météo-France consumer secret (OAuth2)"),
    "FOGOSPT_API_KEY": ("fogospt", "Fogos.pt token, sent as X-API-Key (after access is granted)"),
}

SIGNUP = {
    "firms": "https://firms.modaps.eosdis.nasa.gov/api/map_key",
    "aemet": "https://opendata.aemet.es/centrodedescargas/altaUsuario",
    "meteofrance": "https://portail-api.meteofrance.fr",
    "cds": "https://cds.climate.copernicus.eu/how-to-api",
    "fogospt": "https://source.fogos.pt/api/request-access",
}
PROVIDERS = list(SIGNUP)

FIRMS_STATUS_URL = "https://firms.modaps.eosdis.nasa.gov/mapserver/mapkey_status/?MAP_KEY="
AEMET_CHECK_URL = (
    "https://opendata.aemet.es/opendata/api/valores/climatologicos/"
    "inventarioestaciones/todasestaciones/"
)
METEOFRANCE_TOKEN_URL = "https://portail-api.meteofrance.fr/token"


class ToolError(Exception):
    """A problem the user can fix. Shown as a short message, without a traceback."""


def read_secrets() -> dict[str, str]:
    values: dict[str, str] = {}
    if SECRETS_FILE.exists():
        for line in SECRETS_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                name, value = line.split("=", 1)
                values[name.strip()] = value.strip()
    return values


def write_secrets(values: dict[str, str]) -> None:
    folder = SECRETS_FILE.parent
    if not folder.exists():
        folder.mkdir(parents=True)
        os.chmod(folder, 0o700)
    tmp = SECRETS_FILE.with_name(SECRETS_FILE.name + ".tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write("# Local secrets. Never commit this file.\n")
        for name in sorted(values):
            handle.write(f"{name}={values[name]}\n")
    os.replace(tmp, SECRETS_FILE)


def get_value(name: str, secrets: dict[str, str]) -> str | None:
    return os.environ.get(name) or secrets.get(name) or None


def mask(value: str) -> str:
    return "..." + value[-4:] if len(value) > 8 else "(short)"


def redact(text: str, *secrets: str | None) -> str:
    for secret in secrets:
        if secret:
            text = text.replace(secret, "[hidden]")
    return text


def problem_text(body: str, *secrets: str | None) -> str:
    text = body.strip()
    try:
        data = json.loads(text)
    except ValueError:
        data = None
    if isinstance(data, dict):
        text = str(
            data.get("descripcion")
            or data.get("error_description")
            or data.get("error")
            or text
        )
    return redact(text[:200], *secrets)


def http(
    method: str,
    url: str,
    headers: dict[str, str] | None = None,
    body: bytes | None = None,
) -> tuple[int, str]:
    all_headers = {"User-Agent": f"apikeys/{VERSION}"}
    all_headers.update(headers or {})
    request = urllib.request.Request(url, data=body, headers=all_headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            return response.status, response.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as error:
        return error.code, error.read().decode("utf-8", "replace")
    except urllib.error.URLError as error:
        raise ToolError(f"no answer from the server ({error.reason})") from None


def check_firms(secrets: dict[str, str]) -> str:
    key = get_value("FIRMS_MAP_KEY", secrets)
    if not key:
        return "not set"
    status, body = http("GET", FIRMS_STATUS_URL + urllib.parse.quote(key))
    if status == 200:
        return "OK: " + redact(body.strip()[:200], key)
    return f"REJECTED (HTTP {status}): " + problem_text(body, key)


def check_aemet(secrets: dict[str, str]) -> str:
    key = get_value("AEMET_API_KEY", secrets)
    if not key:
        return "not set"
    status, body = http(
        "GET", AEMET_CHECK_URL, headers={"api_key": key, "Accept": "application/json"}
    )
    if status == 200:
        return "OK"
    return f"REJECTED (HTTP {status}): " + problem_text(body, key)


def meteofrance_token(secrets: dict[str, str]) -> tuple[str, int]:
    key = get_value("METEOFRANCE_CONSUMER_KEY", secrets)
    secret = get_value("METEOFRANCE_CONSUMER_SECRET", secrets)
    if not (key and secret):
        raise ToolError("set METEOFRANCE_CONSUMER_KEY and METEOFRANCE_CONSUMER_SECRET first")
    basic = base64.b64encode(f"{key}:{secret}".encode("utf-8")).decode("ascii")
    status, body = http(
        "POST",
        METEOFRANCE_TOKEN_URL,
        headers={
            "Authorization": f"Basic {basic}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body=urllib.parse.urlencode({"grant_type": "client_credentials"}).encode("ascii"),
    )
    if status != 200:
        raise ToolError(
            f"Météo-France rejected the credentials (HTTP {status}): "
            + problem_text(body, key, secret, basic)
        )
    try:
        data = json.loads(body)
        return str(data["access_token"]), int(data.get("expires_in", 3600))
    except (ValueError, KeyError, TypeError):
        raise ToolError("unexpected answer from the Météo-France token endpoint") from None


def check_meteofrance(secrets: dict[str, str]) -> str:
    if not (
        get_value("METEOFRANCE_CONSUMER_KEY", secrets)
        and get_value("METEOFRANCE_CONSUMER_SECRET", secrets)
    ):
        return "not set"
    _token, seconds = meteofrance_token(secrets)
    return f"OK: token obtained, valid about {seconds // 60} minutes (token not shown)"


def check_cds(_secrets: dict[str, str]) -> str:
    if not CDS_FILE.exists():
        return "not set (no ~/.cdsapirc file)"
    text = CDS_FILE.read_text(encoding="utf-8", errors="replace")
    problems = []
    if "url:" not in text or "key:" not in text:
        problems.append("needs both 'url:' and 'key:' lines")
    mode = CDS_FILE.stat().st_mode & 0o777
    if mode & 0o077:
        problems.append(f"permissions {oct(mode)} are too open (fix: chmod 600 {CDS_FILE})")
    if problems:
        return "WARNING: " + "; ".join(problems)
    return "file looks right (not validated online)"


def check_fogospt(secrets: dict[str, str]) -> str:
    if not get_value("FOGOSPT_API_KEY", secrets):
        return "not set (request access with the form first)"
    return "stored (cannot be checked yet: no public check endpoint)"


CHECKERS = {
    "firms": check_firms,
    "aemet": check_aemet,
    "meteofrance": check_meteofrance,
    "cds": check_cds,
    "fogospt": check_fogospt,
}


def cmd_init(_args: argparse.Namespace) -> int:
    if SECRETS_FILE.exists():
        print(f"Secrets file already exists: {SECRETS_FILE}")
    else:
        write_secrets({})
        print(f"Created {SECRETS_FILE} (only your user can read it).")
    print("Next: apikeys set FIRMS_MAP_KEY   (the value is typed hidden)")
    return 0


def cmd_list(_args: argparse.Namespace) -> int:
    secrets = read_secrets()
    print(f"{'VARIABLE':<30}{'STATUS':<9}{'LAST 4':<10}WHAT IT IS")
    for name, (_provider, description) in VARIABLES.items():
        value = get_value(name, secrets)
        status = "set" if value else "not set"
        shown = mask(value) if value else "-"
        print(f"{name:<30}{status:<9}{shown:<10}{description}")
    cds_status = "present" if CDS_FILE.exists() else "not set"
    print(f"{'(file) ~/.cdsapirc':<30}{cds_status:<9}{'-':<10}Copernicus CDS token")
    print("\nWhere to get each key:")
    for provider, page in SIGNUP.items():
        print(f"  {provider:<12} {page}")
    return 0


def cmd_set(args: argparse.Namespace) -> int:
    if args.name not in VARIABLES:
        raise ToolError(f"unknown variable {args.name!r}. Known: {', '.join(VARIABLES)}")
    if args.stdin:
        value = sys.stdin.readline().strip()
    else:
        value = getpass.getpass(f"Value for {args.name} (hidden): ").strip()
    if not value:
        raise ToolError("empty value, nothing was stored")
    if args.name == "AEMET_API_KEY" and value.count(".") != 2:
        print(
            "Warning: AEMET keys are long strings with two dots (JWT format). "
            "Check that you copied the whole key."
        )
    secrets = read_secrets()
    secrets[args.name] = value
    write_secrets(secrets)
    print(f"Stored {args.name} in {SECRETS_FILE}. The value was not printed.")
    return 0


def cmd_unset(args: argparse.Namespace) -> int:
    secrets = read_secrets()
    if args.name not in secrets:
        print(f"{args.name} is not stored in {SECRETS_FILE}.")
        return 0
    del secrets[args.name]
    write_secrets(secrets)
    print(f"Removed {args.name}.")
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    secrets = read_secrets()
    names = PROVIDERS if args.provider == "all" else [args.provider]
    failed = False
    for name in names:
        try:
            result = CHECKERS[name](secrets)
        except ToolError as error:
            result = f"ERROR: {error}"
        failed = failed or result.startswith(("REJECTED", "ERROR", "WARNING"))
        print(f"{name:<12} {result}")
    return 1 if failed else 0


def cmd_login(_args: argparse.Namespace) -> int:
    _token, seconds = meteofrance_token(read_secrets())
    until = time.strftime("%H:%M", time.localtime(time.time() + seconds))
    print(
        f"Météo-France login OK. Token valid for about {seconds // 60} minutes "
        f"(until {until}). The token was not printed."
    )
    return 0


def cmd_token(_args: argparse.Namespace) -> int:
    token, _seconds = meteofrance_token(read_secrets())
    print("Keep this token private. Do not paste it into chats, issues or logs.", file=sys.stderr)
    print(token)
    return 0


def in_git_work_tree(path: Path) -> bool:
    try:
        result = subprocess.run(
            ["git", "-C", str(path.parent), "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return False
    return result.returncode == 0 and result.stdout.strip() == "true"


def git_ignores(path: Path) -> bool:
    result = subprocess.run(
        ["git", "-C", str(path.parent), "check-ignore", "-q", str(path)],
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def cmd_doctor(_args: argparse.Namespace) -> int:
    problems: list[str] = []
    if SECRETS_FILE.exists():
        mode = SECRETS_FILE.stat().st_mode & 0o777
        if mode & 0o077:
            problems.append(
                f"{SECRETS_FILE} can be read by other users ({oct(mode)}). "
                f"Fix: chmod 600 {SECRETS_FILE}"
            )
        else:
            print(f"OK: {SECRETS_FILE} permissions are {oct(mode)}.")
        if in_git_work_tree(SECRETS_FILE) and not git_ignores(SECRETS_FILE):
            problems.append(
                "the secrets file is inside a git repository and git does not ignore it. "
                "Move it or add it to .gitignore"
            )
    else:
        print("No secrets file yet. Run: apikeys init")
    if CDS_FILE.exists() and (CDS_FILE.stat().st_mode & 0o077):
        problems.append(f"{CDS_FILE} can be read by other users. Fix: chmod 600 {CDS_FILE}")
    for problem in problems:
        print(f"PROBLEM: {problem}")
    if not problems:
        print("No problems found.")
    return 1 if problems else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="apikeys", description="Store, check and use API keys from the terminal."
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="create the local secrets file (never overwrites)")
    sub.add_parser("list", help="show which keys are set (values masked)")

    p_set = sub.add_parser("set", help="store a key (hidden input)")
    p_set.add_argument("name", help="variable name, for example FIRMS_MAP_KEY")
    p_set.add_argument("--stdin", action="store_true", help="read the value from standard input")

    p_unset = sub.add_parser("unset", help="remove a key")
    p_unset.add_argument("name", help="variable name to remove")

    p_check = sub.add_parser("check", help="check keys with one read-only request")
    p_check.add_argument("provider", nargs="?", default="all", choices=PROVIDERS + ["all"])

    p_login = sub.add_parser("login", help="get an OAuth2 token and show its expiry")
    p_login.add_argument("provider", choices=["meteofrance"])

    p_token = sub.add_parser("token", help="print an OAuth2 token to stdout (use with care)")
    p_token.add_argument("provider", choices=["meteofrance"])

    sub.add_parser("doctor", help="check file permissions and git safety")
    return parser


HANDLERS = {
    "init": cmd_init,
    "list": cmd_list,
    "set": cmd_set,
    "unset": cmd_unset,
    "check": cmd_check,
    "login": cmd_login,
    "token": cmd_token,
    "doctor": cmd_doctor,
}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return HANDLERS[args.command](args)
    except ToolError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\ncancelled", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
