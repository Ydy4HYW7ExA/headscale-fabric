import subprocess

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[4]))
from ssh_config import SSH_BASE, REMOTE, ssh_cmd


def run() -> None:
    result = subprocess.run(SSH_BASE + ["docker exec headscale headscale policy get -o json"], check=True, capture_output=True, text=True)
    print(result.stdout)
