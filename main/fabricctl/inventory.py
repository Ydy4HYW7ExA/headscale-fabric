"""Inventory introspection utilities."""
from . import config


def list_hosts() -> list[dict]:
    """Walk the inventory and return a flat list of hosts with group info."""
    inv = config.load_inventory()
    hosts = []

    def walk(data, group=""):
        if not isinstance(data, dict):
            return
        for key, val in data.items():
            if key == "hosts" and isinstance(val, dict):
                for name, props in val.items():
                    props = props or {}
                    hosts.append({
                        "name": name,
                        "group": group,
                        "ansible_host": props.get("ansible_host", ""),
                        "ansible_user": props.get("ansible_user", ""),
                    })
            elif key == "children" and isinstance(val, dict):
                for grp, content in val.items():
                    walk(content, grp)
            else:
                walk(val, group)

    walk(inv.get("all", inv))
    return hosts


def print_hosts() -> None:
    for h in list_hosts():
        print(f"  [{h['group']}] {h['name']:<18} {h['ansible_host']:<45} user={h['ansible_user'] or '?'}")
