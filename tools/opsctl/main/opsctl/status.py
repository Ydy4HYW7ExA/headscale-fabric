import json
import subprocess
from typing import Any

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[4]))
from ssh_config import SSH_BASE, REMOTE, ssh_cmd


def _run(cmd: list[str]) -> str:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    return result.stdout


def _ssh(remote_cmd: str) -> str:
    return _run(SSH_BASE + [remote_cmd])


# ── Active channel: real-time queries ──

def active_local_status() -> dict[str, Any]:
    data = json.loads(_run(["tailscale", "status", "--json"]))
    peers = []
    for peer in data.get("Peer", {}).values():
        peers.append({
            "name": peer.get("DNSName", "").rstrip('.'),
            "os": peer.get("OS"),
            "ip": (peer.get("TailscaleIPs") or [""])[0],
            "online": peer.get("Online"),
        })
    return {
        "self": data["Self"]["DNSName"].rstrip('.'),
        "magic_dns": data["CurrentTailnet"]["MagicDNSEnabled"],
        "peers": peers,
    }


def active_remote_nodes() -> list[dict[str, Any]]:
    out = _ssh("docker exec headscale headscale nodes list -o json")
    data = json.loads(out)
    return [
        {
            "id": item.get("id"),
            "name": item.get("given_name") or item.get("name"),
            "hostname": item.get("name"),
            "ip": (item.get("ip_addresses") or [""])[0],
            "online": item.get("online"),
            "user": item.get("user", {}).get("name"),
        }
        for item in data
    ]


# ── Passive channel: read pre-built snapshots ──

SNAPSHOT_DIR = "/opt/headscale/latest-state"


def passive_nodes() -> list[dict[str, Any]]:
    raw = _ssh(f"cat {SNAPSHOT_DIR}/nodes.json")
    data = json.loads(raw)
    return [
        {
            "id": item.get("id"),
            "name": item.get("given_name") or item.get("name"),
            "hostname": item.get("name"),
            "ip": (item.get("ip_addresses") or [""])[0],
            "online": item.get("online"),
        }
        for item in data
    ]


def passive_policy() -> dict:
    raw = _ssh(f"cat {SNAPSHOT_DIR}/policy.json")
    return json.loads(raw)


def passive_containers() -> str:
    return _ssh(f"cat {SNAPSHOT_DIR}/containers.txt").strip()


def passive_timestamp() -> str:
    return _ssh(f"cat {SNAPSHOT_DIR}/timestamp.txt").strip()


def passive_preauthkeys() -> list[dict]:
    raw = _ssh(f"cat {SNAPSHOT_DIR}/preauthkeys.json")
    return json.loads(raw)


# ── Report rendering ──

def render_report(mode: str = "active") -> str:
    lines = []

    if mode == "passive":
        lines.append("=== Passive Snapshot ===")
        ts = passive_timestamp()
        lines.append(f"snapshot_time: {ts}")
        lines.append("")
        lines.append("nodes:")
        for node in passive_nodes():
            st = "online" if node["online"] else "offline"
            lines.append(f"  {node['name']:<15} {node['ip']:<14} {st}")
        lines.append("")
        lines.append("containers:")
        for line in passive_containers().splitlines():
            lines.append(f"  {line}")
        return "\n".join(lines)

    # Active mode (default): real-time from both channels
    local = active_local_status()
    remote = active_remote_nodes()

    lines.append("=== Tailnet Status ===")
    lines.append(f"self: {local['self']}")
    lines.append(f"magic_dns: {local['magic_dns']}")
    lines.append("")

    lines.append("=== Control Plane (Headscale) ===")
    for node in remote:
        st = "online" if node["online"] else "offline"
        lines.append(f"  {node['name']:<15} {node['ip']:<14} {st:<8} user={node['user']}")
    lines.append("")

    lines.append("=== Local View (tailscale status) ===")
    for peer in local["peers"]:
        st = "online" if peer["online"] else "offline"
        lines.append(f"  {peer['name']:<45} {peer['ip']:<14} {st:<8} os={peer['os']}")

    # Also show latest snapshot timestamp for reference
    try:
        ts = passive_timestamp()
        lines.append("")
        lines.append(f"latest_snapshot: {ts}")
    except Exception:
        pass

    return "\n".join(lines)


def run(mode: str = "active") -> None:
    print(render_report(mode))
