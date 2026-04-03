"""List and inspect remote backups."""
import subprocess

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[4]))
from ssh_config import SSH_BASE, REMOTE, ssh_cmd


def _ssh(cmd: str) -> str:
    result = subprocess.run(SSH_BASE + [cmd], capture_output=True, text=True)
    return result.stdout.strip()


def run() -> None:
    print("=== Remote Backups ===")
    dirs = _ssh("ls -d /opt/headscale/backups/*/ 2>/dev/null | sort")
    if dirs:
        for d in dirs.splitlines():
            d = d.rstrip("/")
            name = d.split("/")[-1]
            state_files = _ssh(f"ls {d}/state/ 2>/dev/null")
            files_count = _ssh(f"find {d}/files -type f 2>/dev/null | wc -l")
            print(f"  {name}  state=[{state_files.replace(chr(10), ', ')}]  files={files_count}")
    else:
        print("  (no backups found)")

    print()
    print("=== Latest Snapshot ===")
    ts = _ssh("cat /opt/headscale/latest-state/timestamp.txt 2>/dev/null")
    print(f"  timestamp: {ts or '(none)'}")
    snapshot_files = _ssh("ls /opt/headscale/latest-state/ 2>/dev/null")
    if snapshot_files:
        print(f"  files: {snapshot_files.replace(chr(10), ', ')}")
