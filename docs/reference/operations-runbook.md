# Operations Runbook

## 日常状态检查

### 主动查看全网状态（实时）
```bash
cd ~/work/repositories/headscale-fabric/tools/opsctl/main
PYTHONPATH=. python3 opsctl/cli.py status
```

### 被动查看快照状态（最近 5 分钟内）
```bash
cd ~/work/repositories/headscale-fabric/tools/opsctl/main
PYTHONPATH=. python3 opsctl/cli.py status --passive
```

### 查看预授权密钥
```bash
PYTHONPATH=. python3 opsctl/cli.py keys
```

### 查看当前 ACL 策略
```bash
PYTHONPATH=. python3 opsctl/cli.py policy
```

## 部署与变更

### 部署/更新 Headscale
```bash
cd ~/work/repositories/headscale-fabric
python3 main/fabricctl/cli.py deploy
```
底层调用 `scripts/ansible/playbooks/deploy-headscale.yml`。

### 应用 ACL 策略
```bash
python3 main/fabricctl/cli.py apply-policy
```
底层调用 `scripts/ansible/playbooks/apply-policy.yml`。策略模板在 `assets/templates/headscale/policy.json.j2`。

### 备份
```bash
python3 main/fabricctl/cli.py backup
```
服务器侧备份存储在 `/opt/headscale/backups/<timestamp>/`，包含：
- `files/` — 配置、compose、Caddyfile、数据库、密钥、门户文件
- `state/` — 运行时快照（nodes、policy、容器状态、preauthkeys）

## 状态数据源

| 数据源 | 位置 | 更新频率 |
|---|---|---|
| tailscale status | 本机 `tailscale status --json` | 实时 |
| headscale nodes list | 服务器 `docker exec headscale ...` | 实时 |
| 被动快照 | 服务器 `/opt/headscale/latest-state/` | 每 5 分钟 (cron) |
| 历史备份 | 服务器 `/opt/headscale/backups/` | 手动触发 |
| 规划草案 | 服务器 `/opt/headscale/planned/` | 手动编辑 |

## 节点管理

### 添加新 Ubuntu 节点
```bash
ansible-playbook -i scripts/ansible/inventories/production/hosts.yml \
  scripts/ansible/playbooks/add-ubuntu-node.yml
```

### 节点命名规则
- 格式：`<os>-<序号>`，如 `ubuntu-1`、`mac-1`、`win-1`
- 主控机固定为 `ubuntu-master`
- 控制面服务器固定为 `ubuntu-0`
- 详见 `docs/explanation/naming-convention.md`

## 服务器迁移

1. 在旧服务器执行备份：`fabricctl backup`
2. 在新服务器执行 bootstrap：`scripts/ansible/playbooks/bootstrap-server.yml`
3. 恢复数据库和配置从备份
4. 更新 Ansible inventory 中的 `ubuntu-0` IP
5. 用 `opsctl status --passive` 验证快照中的节点信息，作为重建基线
6. 逐个节点重新指向新控制面
