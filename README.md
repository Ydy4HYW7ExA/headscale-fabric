# headscale-fabric

以本机为主控机的 Headscale 部署与运维仓库。

## 快速上手

```bash
# 1. 配置敏感信息
cp .env.example .env
# 编辑 .env，填入服务器 IP、密码、域名等

# 2. 安装依赖
scripts/bootstrap/init-local-control-host.sh

# 3. 查看状态
make status
```

## 前提依赖

- Python 3.10+、pip（pyyaml）
- Ansible Core
- sshpass
- Docker（控制面服务器上）
- Tailscale（所有节点上）

## 目标

- 从本机统一部署和运维 Headscale / Caddy / downloads 门户
- 统一节点命名：ubuntu-master / ubuntu-1 / mac-1 / win-1
- 用 Ansible 做部署编排，尽量零自研
- 用轻量 CLI 和运维工具统一入口
- 所有节点配备看门狗守护，时刻保持在网

## 目录

- `assets/` — 模板（Headscale / Caddy / 门户 / SSH / 看门狗）、示例
- `docs/` — Diataxis 文档（tutorials / how-to / explanation / reference）
- `scripts/` — Ansible playbook、bootstrap、render helpers
- `tools/` — 运维工具（opsctl）
- `main/` — 主控 CLI（fabricctl）

## 敏感信息

所有密码、IP、域名等敏感信息存放在 `.env` 文件中（git-ignored）。  
模板参见 `.env.example`。
