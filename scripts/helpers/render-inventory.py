#!/usr/bin/env python3
"""Pretty-print the production inventory for review."""
from pathlib import Path

try:
    import yaml
except ImportError:
    raise SystemExit("pip install pyyaml")

ROOT = Path(__file__).resolve().parents[2]
INV = ROOT / "scripts" / "ansible" / "inventories" / "production" / "hosts.yml"

data = yaml.safe_load(INV.read_text())


def walk(obj, indent=0):
    if not isinstance(obj, dict):
        return
    for key, val in obj.items():
        if key == "hosts" and isinstance(val, dict):
            for host, props in val.items():
                props = props or {}
                h = props.get("ansible_host", "?")
                u = props.get("ansible_user", "?")
                print(f"{'  ' * indent}{host:<18}  host={h}  user={u}")
        elif key == "children" and isinstance(val, dict):
            for grp, content in val.items():
                print(f"{'  ' * indent}[{grp}]")
                walk(content, indent + 1)
        else:
            walk(val, indent)


walk(data.get("all", data))
