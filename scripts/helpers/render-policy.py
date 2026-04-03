#!/usr/bin/env python3
"""Render policy.json from Jinja2 template using inventory-derived hosts and current ACL rules.

Usage: python3 scripts/helpers/render-policy.py

The template expects two variables:
  - hosts: dict mapping node names to IP/32 CIDRs
  - acls: list of ACL rule dicts

Since IPs are assigned by Headscale at runtime and are not in the inventory,
this script reads the current node IPs from the server snapshot if available,
or falls back to a skeleton with placeholder IPs.
"""
import json
import subprocess
from pathlib import Path

try:
    import jinja2
    import yaml
except ImportError:
    raise SystemExit("pip install jinja2 pyyaml")

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "assets" / "templates" / "headscale" / "policy.json.j2"
VARS = ROOT / "scripts" / "ansible" / "inventories" / "production" / "group_vars" / "all.yml"
INV = ROOT / "scripts" / "ansible" / "inventories" / "production" / "hosts.yml"

# Import SSH config from shared module
import sys as _sys
_sys.path.insert(0, str(ROOT))
from ssh_config import SSH_BASE, REMOTE, ssh_cmd


def get_live_hosts() -> dict[str, str]:
    """Read node name->IP mapping from server snapshot or live query."""
    try:
        result = subprocess.run(
            SSH_BASE + ["cat /opt/headscale/latest-state/nodes.json 2>/dev/null"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            nodes = json.loads(result.stdout)
            return {
                (n.get("given_name") or n.get("name")): f"{(n.get('ip_addresses') or ['?'])[0]}/32"
                for n in nodes
            }
    except Exception:
        pass
    return {}


def default_acls(hosts: dict) -> list[dict]:
    """Generate default ACL rules matching current production policy pattern."""
    master_nodes = [n for n in hosts if "master" in n or n.startswith("ubuntu-")]
    mac_nodes = [n for n in hosts if n.startswith("mac-")]
    win_nodes = [n for n in hosts if n.startswith("win-")]

    acls = []
    # ubuntu-master and ubuntu nodes can access everything
    if master_nodes:
        acls.append({"action": "accept", "src": master_nodes, "dst": ["*:*"]})
    # mac nodes can access ubuntu SSH and win all ports
    if mac_nodes:
        dst = [f"{n}:22" for n in hosts if n.startswith("ubuntu-")] + [f"{n}:*" for n in win_nodes]
        if dst:
            acls.append({"action": "accept", "src": mac_nodes, "dst": dst})
    # win nodes can access ubuntu SSH and mac all ports
    if win_nodes:
        dst = [f"{n}:22" for n in hosts if n.startswith("ubuntu-")] + [f"{n}:*" for n in mac_nodes]
        if dst:
            acls.append({"action": "accept", "src": win_nodes, "dst": dst})
    return acls


hosts = get_live_hosts()
if not hosts:
    # Fallback: read inventory and use placeholder IPs
    inv = yaml.safe_load(INV.read_text())
    def walk(data):
        result = {}
        if not isinstance(data, dict):
            return result
        for key, val in data.items():
            if key == "hosts" and isinstance(val, dict):
                for name in val:
                    result[name] = f"100.64.0.0/32"  # placeholder
            elif key == "children" and isinstance(val, dict):
                for content in val.values():
                    result.update(walk(content))
            else:
                result.update(walk(val))
        return result
    hosts = walk(inv.get("all", inv))

acls = default_acls(hosts)

env = jinja2.Environment(loader=jinja2.FileSystemLoader(str(TEMPLATE.parent)))
tmpl = env.get_template(TEMPLATE.name)
rendered = tmpl.render(hosts=hosts, acls=acls)

# Validate output is valid JSON
json.loads(rendered)
print(rendered)
