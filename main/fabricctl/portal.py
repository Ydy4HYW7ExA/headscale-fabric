"""Downloads portal management: check portal status, list portal files."""
import subprocess

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from ssh_config import SSH_BASE, REMOTE, ssh_cmd


def _ssh(cmd: str) -> str:
    result = subprocess.run(SSH_BASE + [cmd], capture_output=True, text=True)
    return result.stdout.strip()


def list_portal_files() -> list[str]:
    raw = _ssh("ls /var/www/headscale-downloads/ 2>/dev/null")
    return raw.splitlines() if raw else []


def print_portal_status() -> None:
    files = list_portal_files()
    if files:
        print("portal files:")
        for f in files:
            print(f"  {f}")
    else:
        print("  (portal unreachable or empty)")

    url = _ssh("cat /opt/headscale/latest-state/containers.txt 2>/dev/null | grep caddy")
    if url:
        print(f"caddy: {url}")
