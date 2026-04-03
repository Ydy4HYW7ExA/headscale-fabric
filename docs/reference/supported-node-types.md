# Supported node types

## 当前支持

| OS | 接入方式 | 安装脚本 | Ansible 管理 |
|---|---|---|---|
| Ubuntu / Debian | 门户脚本 或 Ansible | `install-linux.sh` | 完整支持 |
| macOS | 门户脚本 | `install-mac.sh` | SSH 可达，playbook 有限 |
| Windows | 门户脚本（CMD） | `join-windows.cmd` | SSH 不可达，需手动操作 |

## 各 OS 的能力差异

### Ubuntu

- SSH 免密：支持（通过 `sync-ubuntu-user-env.yml` 分发公钥）
- Ansible 全功能：支持
- tailscale CLI：`/usr/bin/tailscale`
- 看门狗守护：支持（安装脚本自动部署）

### macOS

- SSH 免密：支持（需手动或脚本在 Mac 上添加 authorized_keys）
- Ansible：基础功能可用，但 `apt` 模块不可用
- tailscale CLI：`/usr/local/bin/tailscale` 或通过 App
- 看门狗守护：支持（安装脚本自动部署）

### Windows

- SSH 免密：有限（需要 OpenSSH Server，配置较复杂）
- Ansible：需要 WinRM，当前未配置
- tailscale CLI：`tailscale.exe`（安装后在 PATH 中）
- RDP：可通过 tailnet IP 远程桌面
- 看门狗守护：支持（安装脚本自动部署）

## 扩展新 OS

1. 在 inventory 中新增 `<os>_nodes` 组
2. 在 `assets/templates/downloads/` 中新增安装脚本模板
3. 在 `host_vars/` 中新增节点文件
4. 命名遵循 `<os>-<N>` 格式
