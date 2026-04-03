# Inventory schema

## 文件位置

`scripts/ansible/inventories/production/hosts.yml`

## 结构

```yaml
all:
  children:
    control_plane:        # 控制面服务器（运行 Headscale + Caddy）
      hosts:
        ubuntu-0:
          ansible_host: <公网IP>
          ansible_user: root
    operator_hosts:       # 主控机
      hosts:
        ubuntu-master:
          ansible_host: <tailnet DNS>
          ansible_user: h
    ubuntu_nodes:         # Ubuntu 受管节点
      hosts:
        ubuntu-1:
          ansible_host: <tailnet DNS>
          ansible_user: <user>
    mac_nodes:            # macOS 节点
      hosts:
        mac-1:
          ansible_host: <tailnet DNS>
          ansible_user: <user>
    windows_nodes:        # Windows 节点
      hosts:
        win-1:
          ansible_host: <tailnet DNS>
```

## 字段说明

| 字段 | 说明 |
|---|---|
| `ansible_host` | 控制面用公网 IP，其他节点用 tailnet DNS 名（`<name>.tailnet.<domain>`） |
| `ansible_user` | SSH 登录用户名 |

## group_vars

| 文件 | 内容 |
|---|---|
| `all.yml` | `headscale_domain`、`tailnet_suffix`、镜像 digest |
| `control_plane.yml` | `downloads_root` 等控制面专用变量 |
| `nodes.yml` | `ssh_primary_user` 等节点通用变量 |

## host_vars

每个节点一个文件（如 `host_vars/ubuntu-1.yml`），包含：
- `node_name` — 节点显示名
- `node_role` — 角色（`control-plane` / `operator-host` / `managed-node`）
