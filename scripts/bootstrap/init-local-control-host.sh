#!/usr/bin/env bash
set -euo pipefail
# Initialize the local operator host (ubuntu-master) for headscale-fabric.
# Run this once after cloning the repo.

echo "=== Checking dependencies ==="

# Python
command -v python3 >/dev/null || { echo "ERROR: python3 required"; exit 1; }

# pip packages
pip3 install --user --break-system-packages pyyaml jinja2 2>/dev/null || pip3 install --user pyyaml jinja2

# Ansible
if ! command -v ansible-playbook >/dev/null 2>&1; then
    if command -v pipx >/dev/null 2>&1; then
        pipx install ansible-core
    else
        pip3 install --user --break-system-packages ansible-core 2>/dev/null || pip3 install --user ansible-core
    fi
    echo "NOTE: ansible installed to ~/.local/bin — ensure it's on PATH"
fi

# sshpass
if ! command -v sshpass >/dev/null 2>&1; then
    echo "Installing sshpass..."
    sudo apt-get install -y sshpass 2>/dev/null || brew install sshpass 2>/dev/null || echo "WARN: sshpass not installed"
fi

# tailscale
if ! command -v tailscale >/dev/null 2>&1; then
    echo "WARN: tailscale not installed — install from https://tailscale.com/download"
fi

# SSH key
if [ ! -f ~/.ssh/id_ed25519 ]; then
    echo "Generating SSH key..."
    ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N ""
fi

echo ""
echo "=== Ready ==="
echo "Run: cd $(dirname "$0")/../.."
echo "     python3 main/fabricctl/cli.py status"
