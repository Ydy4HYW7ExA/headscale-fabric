"""Policy management: get, validate, apply ACL policy."""
import json
import subprocess

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from ssh_config import SSH_BASE, REMOTE, ssh_cmd


def _ssh(cmd: str) -> str:
    result = subprocess.run(SSH_BASE + [cmd], capture_output=True, text=True)
    return result.stdout.strip()


def get_policy() -> dict:
    raw = _ssh("docker exec headscale headscale policy get -o json 2>/dev/null")
    return json.loads(raw) if raw else {}


def print_policy() -> None:
    p = get_policy()
    print(json.dumps(p, indent=2, ensure_ascii=False))


def validate_planned() -> str:
    return _ssh("docker exec headscale headscale policy check -f /tmp/policy.next.json 2>&1")
