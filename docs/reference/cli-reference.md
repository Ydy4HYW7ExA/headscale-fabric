# CLI Reference

## fabricctl — 主控 CLI

入口：`python3 main/fabricctl/cli.py <command>`

| 命令 | 说明 | 底层 |
|---|---|---|
| `status` | 显示 inventory 节点列表、控制面容器健康状态、全网在线节点、最新快照时间 | SSH 查询控制面 |
| `deploy` | 部署/更新 Headscale 全栈（模板下发、容器拉取启动、cron 注册、快照） | playbook: deploy-headscale.yml |
| `backup` | 备份控制面（配置、数据库、密钥、状态快照） | playbook: backup-headscale.yml |
| `apply-policy` | 验证并应用 ACL 策略草案 | playbook: apply-policy.yml |

### fabricctl status 输出

- `Inventory Nodes` — 按组列出 inventory 中所有节点（名称、ansible_host、user）
- `Control Plane` — 控制面 Docker 容器运行状态
- `Online Nodes` — Headscale 控制面视角的全部注册节点（名称、IP、在线状态）
- `latest_snapshot` — 服务器被动快照的最新时间戳

## opsctl — 运维 CLI

入口：`cd tools/opsctl/main && PYTHONPATH=. python3 opsctl/cli.py <command>`

| 命令 | 说明 |
|---|---|
| `status` | 主动采集全网状态：本机 tailscale 视角 + 控制面 headscale 视角，同时显示最新快照时间 |
| `status --passive` | 被动读取服务器快照（/opt/headscale/latest-state/），不执行实时查询 |
| `keys` | 列出预授权密钥（ID、是否 reusable、过期时间） |
| `policy` | 显示当前生效的 ACL 策略 JSON |
| `portal` | 显示门户文件列表、URL、Caddy 运行状态 |
| `backup` | 列出远程备份目录和最新快照信息 |

### status 输出字段

**Active 模式**（默认）：
- `Tailnet Status` — 本机 DNS 名、MagicDNS 状态
- `Control Plane` — 控制面视角的全部注册节点（名称、IP、在线、用户）
- `Local View` — 本机 tailscale 视角的 peer（DNS 名、IP、在线、OS）
- `latest_snapshot` — 最新被动快照的时间戳

**Passive 模式**：
- `snapshot_time` — 快照生成时间
- `nodes` — 快照中的全部节点
- `containers` — 快照中的 Docker 容器运行状态

### 数据来源

| 通道 | 数据源 | 延迟 |
|---|---|---|
| 主动/本机 | `tailscale status --json` | 实时 |
| 主动/控制面 | `docker exec headscale headscale nodes list -o json` | 实时（需 SSH） |
| 被动 | `/opt/headscale/latest-state/*.json` | ≤5 分钟 |
