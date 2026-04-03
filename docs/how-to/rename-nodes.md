# Rename nodes

## 命名规范

- `ubuntu-master` — 主控机（固定）
- `ubuntu-0` — 控制面服务器（固定）
- `ubuntu-<N>` — Ubuntu 受管节点
- `mac-<N>` — macOS 节点
- `win-<N>` — Windows 节点

## 重命名步骤

### 1. 在 Headscale 中重命名

```bash
# 查看当前节点列表和 ID
ssh root@<SERVER_IP> "docker exec headscale headscale nodes list -u default"

# 重命名
ssh root@<SERVER_IP> "docker exec headscale headscale nodes rename -i <NODE_ID> <新名称>"
```

### 2. 更新 inventory

编辑 `scripts/ansible/inventories/production/hosts.yml`，修改对应节点名称。如果节点组变了，也要调整。

### 3. 更新 host_vars

重命名 `host_vars/<旧名>.yml` 为 `host_vars/<新名>.yml`，更新 `node_name` 字段。

### 4. 更新 SSH 别名

修改主控机 `~/.ssh/config` 中的对应别名。

### 5. 更新快照

```bash
ssh root@<SERVER_IP> "/opt/headscale/snapshot.sh"
```
