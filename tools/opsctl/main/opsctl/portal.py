"""Check downloads portal status and files."""
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from ssh_config import SSH_BASE


def _ssh(cmd: str) -> str:
    result = subprocess.run(SSH_BASE + [cmd], capture_output=True, text=True)
    return result.stdout.strip()


def run() -> None:
    print("=== Portal Files ===")
    files = _ssh("ls -la /opt/headscale/downloads/ 2>/dev/null")
    if files:
        for line in files.splitlines():
            print(f"  {line}")
    else:
        print("  (unreachable)")

    print()
    print("=== Portal URL ===")
    domain = os.environ.get("HEADSCALE_DOMAIN", "")
    if domain:
        print(f"  https://{domain}/downloads/")
    else:
        print("  (HEADSCALE_DOMAIN not set in .env)")

    print()
    print("=== Caddy Status ===")
    caddy = _ssh("docker ps --filter name=caddy --format '{{.Names}}: {{.Status}}' 2>/dev/null")
    print(f"  {caddy or '(unreachable)'}")
