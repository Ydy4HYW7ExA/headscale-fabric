# Back up and restore

## 备份

### 通过 fabricctl

```bash
python3 main/fabricctl/cli.py backup
```

底层调用 `backup-headscale.yml`，在服务器 `/opt/headscale/backups/<timestamp>/` 下创建：
- `files/` — config、docker-compose、Caddyfile、downloads、数据库、密钥
- `state/` — nodes、policy、preauthkeys、容器状态

### 查看备份列表

```bash
cd tools/opsctl/main && PYTHONPATH=. python3 opsctl/cli.py backup
```

## 恢复

### 恢复到同一台服务器

```bash
# 停止容器
ssh root@<SERVER_IP> "cd /opt/headscale && docker compose down"

# 从备份恢复
ssh root@<SERVER_IP> "cp -a /opt/headscale/backups/<timestamp>/files/config /opt/headscale/"
ssh root@<SERVER_IP> "cp -a /opt/headscale/backups/<timestamp>/files/data /opt/headscale/"

# 重启
ssh root@<SERVER_IP> "cd /opt/headscale && docker compose up -d"
```

### 恢复到新服务器

1. 先运行 `bootstrap-server.yml` 初始化新服务器
2. 停止容器
3. 将备份中的 `data/` 目录（含 SQLite 数据库和密钥）复制到新服务器
4. 恢复 config
5. 重启容器
6. 更新 inventory 中的服务器 IP
7. 各节点需要重新指向新控制面
