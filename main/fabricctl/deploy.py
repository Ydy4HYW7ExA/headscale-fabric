"""Deploy helpers: template rendering and pre-deploy checks."""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = ROOT / "assets" / "templates"

import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ssh_config import SSH_BASE, REMOTE, ssh_cmd


def _ssh(cmd: str) -> str:
    result = subprocess.run(SSH_BASE + [cmd], capture_output=True, text=True)
    return result.stdout.strip()


def check_server_health() -> dict:
    """Quick health check of the control plane server."""
    containers = _ssh("docker ps --filter name=headscale --format '{{.Names}}: {{.Status}}' 2>/dev/null")
    headscale_ok = _ssh("docker exec headscale headscale nodes list -o json > /dev/null 2>&1 && echo ok")
    return {
        "containers": containers.splitlines() if containers else [],
        "headscale_responsive": headscale_ok == "ok",
    }


def list_templates() -> list[str]:
    """List all j2 templates in the repo."""
    return sorted(str(p.relative_to(ROOT)) for p in TEMPLATES.rglob("*.j2"))


def print_pre_deploy_check() -> None:
    health = check_server_health()
    print("server health:")
    for c in health["containers"]:
        print(f"  {c}")
    print(f"  headscale responsive: {health['headscale_responsive']}")
    print()
    print("templates:")
    for t in list_templates():
        print(f"  {t}")
