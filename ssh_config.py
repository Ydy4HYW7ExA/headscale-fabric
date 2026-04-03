"""Shared SSH connection config — reads credentials from .env file."""
import os
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[0]


def _load_env() -> None:
    """Load .env file into os.environ if not already set."""
    env_file = _ROOT / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, val = line.partition("=")
        key, val = key.strip(), val.strip()
        if key and key not in os.environ:
            os.environ[key] = val


_load_env()

SERVER_HOST = os.environ.get("HEADSCALE_SERVER_HOST", "")
SERVER_USER = os.environ.get("HEADSCALE_SERVER_USER", "root")
SERVER_PASS = os.environ.get("HEADSCALE_SERVER_PASS", "")

REMOTE = f"{SERVER_USER}@{SERVER_HOST}"
SSH_BASE = ["sshpass", "-p", SERVER_PASS, "ssh", "-o", "StrictHostKeyChecking=no", REMOTE]


def ssh_cmd(remote_cmd: str) -> list[str]:
    """Return full SSH command list for running a command on the control plane."""
    return SSH_BASE + [remote_cmd]
