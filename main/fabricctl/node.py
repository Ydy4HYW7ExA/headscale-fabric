"""Node management: list, inspect, rename nodes via headscale CLI."""
import json
import subprocess

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from ssh_config import SSH_BASE, REMOTE, ssh_cmd


def _ssh(cmd: str) -> str:
    result = subprocess.run(SSH_BASE + [cmd], capture_output=True, text=True)
    return result.stdout.strip()


def list_nodes() -> list[dict]:
    raw = _ssh("docker exec headscale headscale nodes list -o json 2>/dev/null")
    if not raw:
        return []
    return json.loads(raw)


def print_nodes() -> None:
    nodes = list_nodes()
    if not nodes:
        print("  (no nodes or unreachable)")
        return
    for n in nodes:
        name = n.get("given_name") or n.get("name")
        ip = (n.get("ip_addresses") or ["?"])[0]
        online = "online" if n.get("online") else "offline"
        print(f"  {name:<15} {ip:<14} {online}")


def rename_node(node_id: int, new_name: str) -> str:
    return _ssh(f"docker exec headscale headscale nodes rename -i {node_id} {new_name}")
