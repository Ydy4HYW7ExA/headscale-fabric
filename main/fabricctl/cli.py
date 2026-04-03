import os
import re
import subprocess
import sys
from pathlib import Path

from fabricctl import node, deploy

ROOT = Path(__file__).resolve().parents[2]
PLAYBOOKS = ROOT / "scripts" / "ansible" / "playbooks"
INV = ROOT / "scripts" / "ansible" / "inventories" / "production" / "hosts.yml"
CFG = ROOT / "scripts" / "ansible" / "ansible.cfg"

sys.path.insert(0, str(ROOT))
from ssh_config import SSH_BASE, REMOTE


def _ssh(cmd: str) -> str:
    result = subprocess.run(SSH_BASE + [cmd], capture_output=True, text=True)
    return result.stdout.strip()


def _run_playbook(name: str, extra_args=None) -> None:
    cmd = ["ansible-playbook", "-i", str(INV), str(PLAYBOOKS / name)]
    if extra_args:
        cmd.extend(extra_args)
    env = {**os.environ, "ANSIBLE_CONFIG": str(CFG)}
    subprocess.run(cmd, check=True, env=env)


def _resolve_jinja_env(val: str) -> str:
    """Resolve simple {{ lookup('env', 'VAR') }} patterns using os.environ."""
    match = re.search(r"lookup\(['\"]env['\"],\s*['\"](\w+)['\"]\)", str(val))
    if match:
        return os.environ.get(match.group(1), str(val))
    return str(val)


def cmd_status() -> None:
    import yaml
    inv_data = yaml.safe_load(INV.read_text())

    print("=== Inventory Nodes ===")
    def walk_hosts(data, prefix=""):
        if isinstance(data, dict):
            for key, val in data.items():
                if key == "hosts" and isinstance(val, dict):
                    for host, props in val.items():
                        h = _resolve_jinja_env(props.get("ansible_host", "?")) if props else "?"
                        u = props.get("ansible_user", "?") if props else "?"
                        print(f"  {host:<18} host={h:<45} user={u}")
                elif key == "children" and isinstance(val, dict):
                    for group, content in val.items():
                        print(f"  [{group}]")
                        walk_hosts(content, prefix + "  ")
                else:
                    walk_hosts(val, prefix)
    walk_hosts(inv_data.get("all", inv_data))

    print()
    print("=== Control Plane ===")
    deploy.print_pre_deploy_check()

    print()
    print("=== Online Nodes ===")
    node.print_nodes()

    print()
    ts = _ssh("cat /opt/headscale/latest-state/timestamp.txt 2>/dev/null")
    print(f"latest_snapshot: {ts or '(none)'}")


def cmd_deploy() -> None:
    _run_playbook("deploy-headscale.yml")


def cmd_backup() -> None:
    _run_playbook("backup-headscale.yml")


def cmd_apply_policy() -> None:
    _run_playbook("apply-policy.yml")


def main() -> None:
    commands = {
        "status": cmd_status,
        "deploy": cmd_deploy,
        "backup": cmd_backup,
        "apply-policy": cmd_apply_policy,
    }
    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        names = " | ".join(commands)
        print(f"usage: fabricctl [{names}]")
        raise SystemExit(1)
    commands[sys.argv[1]]()


if __name__ == "__main__":
    main()
