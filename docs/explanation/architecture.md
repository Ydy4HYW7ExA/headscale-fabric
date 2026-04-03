# Architecture

`headscale-fabric` 采用三层结构管理内网穿透网络。

## 三层拓扑

### 1. 主控机 (`ubuntu-master` / 100.64.0.2)

- 保存本仓库源码、Ansible inventory、配置模板和运维工具。
- 通过 `fabricctl` 触发部署、备份、策略应用等 Ansible playbook。
- 通过 `opsctl` 主动/被动采集全网状态。
- 对所有节点拥有单向 SSH 免密权限。
- 是唯一的操作入口——所有变更从这里发起。

### 2. 控制面服务器 (`ubuntu-0` / <SERVER_IP>)

- 公网机器，运行 Headscale（自建 Tailscale 控制面）+ Caddy 反代。
- 提供 downloads 门户供新节点一键接入。
- 持久化目录结构：
  - `/opt/headscale/config/` — Headscale 配置
  - `/opt/headscale/data/` — SQLite 数据库、密钥
  - `/opt/headscale/planned/` — 待应用的策略/compose 草案
  - `/opt/headscale/backups/<timestamp>/` — 定期备份（files + state）
  - `/opt/headscale/latest-state/` — 每 5 分钟自动快照（cron）
- Docker 容器：`headscale`（控制面）、`headscale-caddy`（反代 + 门户）。

### 3. 受管节点

| 名称 | IP | OS | 角色 |
|---|---|---|---|
| `ubuntu-master` | 100.64.0.2 | Linux | 主控机（同时也是 tailnet 节点） |
| `mac-1` | 100.64.0.1 | macOS | 开发机 |
| `win-1` | 100.64.0.3 | Windows | 工作站 |
| `ubuntu-1` | 100.64.0.4 | Linux | 服务器 |

## 状态采集双通道

### 主动采集（实时）

主控机直接查询两个数据源：

1. **本机视角**：`tailscale status --json` — 看到所有 peer 的连通性和延迟。
2. **控制面视角**：SSH 到 ubuntu-0 执行 `docker exec headscale headscale nodes list -o json` — 看到注册的全部节点及其 online 状态。

命令：`opsctl status`（默认 active 模式）

### 被动采集（快照）

服务器每 5 分钟通过 cron 执行 `/opt/headscale/snapshot.sh`，将当前状态写入 `/opt/headscale/latest-state/`：

- `nodes.json` — 全量节点信息（含密钥、IP、在线状态）
- `policy.json` — 当前生效的 ACL 策略
- `preauthkeys.json` — 预授权密钥
- `containers.txt` — Docker 容器运行状态
- `timestamp.txt` — 快照时间戳

命令：`opsctl status --passive`

被动通道的价值：即使 Docker exec 临时不可用，主控机仍能通过快照掌握最近一次的全局状态。服务器迁移时，快照数据可直接作为重建基线。

## 看门狗守护

每个节点上安装了看门狗脚本，每分钟检查 tailscale 是否正常运行：
- Linux：cron 运行 `/usr/local/bin/headscale-watchdog.sh`
- macOS：cron 运行 `/usr/local/bin/headscale-watchdog.sh`
- Windows：Task Scheduler 运行 `C:\headscale-fabric\watchdog.cmd`

检测逻辑：
1. 读取开关文件，如果是 `false` 则跳过
2. 检查 `tailscale status` 的 BackendState
3. 如果不是 `Running`，执行 `tailscale up` 重新连接
4. 记录日志到 `/var/log/headscale-watchdog.log`（Linux/macOS）或 `C:\headscale-fabric\watchdog.log`（Windows）

开关文件：
- Linux/macOS: `/etc/headscale-fabric/watchdog.enabled`
- Windows: `C:\headscale-fabric\watchdog.enabled`
- 写入 `false` 禁用，写入 `true` 启用

看门狗由一键安装脚本自动部署，模板位于 `assets/templates/watchdog/`。

## 仓库目录职责

| 目录 | 职责 |
|---|---|
| `assets/templates/` | 配置模板（Headscale/Caddy/downloads/SSH），唯一模板来源 |
| `scripts/ansible/` | Ansible inventory + playbook，执行部署/备份/策略 |
| `scripts/helpers/` | 轻量渲染辅助脚本（生成 policy/downloads/inventory） |
| `scripts/bootstrap/` | 初始化脚本（安装 Ansible、初始化主控机） |
| `main/fabricctl/` | 主控 CLI，触发 Ansible playbook |
| `tools/opsctl/` | 运维 CLI，读状态/列节点/看 key/看 ACL |
| `docs/` | diataxis 结构文档（tutorials/how-to/explanation/reference） |
