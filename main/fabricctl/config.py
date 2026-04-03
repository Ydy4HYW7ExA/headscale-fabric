"""Fabric configuration loader."""
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INV_FILE = ROOT / "scripts" / "ansible" / "inventories" / "production" / "hosts.yml"
GROUP_VARS = ROOT / "scripts" / "ansible" / "inventories" / "production" / "group_vars" / "all.yml"


def load_inventory() -> dict:
    return yaml.safe_load(INV_FILE.read_text())


def load_global_vars() -> dict:
    return yaml.safe_load(GROUP_VARS.read_text())


def server_ssh_base() -> list[str]:
    """Return SSH command prefix for the control plane server."""
    inv = load_inventory()
    host = inv["all"]["children"]["control_plane"]["hosts"]["ubuntu-0"]["ansible_host"]
    user = inv["all"]["children"]["control_plane"]["hosts"]["ubuntu-0"]["ansible_user"]
    # For now use sshpass; migrate to key-based once available
    return ["ssh", "-o", "StrictHostKeyChecking=no", f"{user}@{host}"]
