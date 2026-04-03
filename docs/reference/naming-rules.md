# Naming rules

## 节点命名

| 角色 | 格式 | 示例 |
|---|---|---|
| 主控机 | `ubuntu-master` | 固定 |
| 控制面 | `ubuntu-0` | 固定 |
| Ubuntu 节点 | `ubuntu-<N>` | `ubuntu-1`, `ubuntu-2` |
| macOS 节点 | `mac-<N>` | `mac-1`, `mac-2` |
| Windows 节点 | `win-<N>` | `win-1`, `win-2` |

## Ansible 组命名

| 组名 | 包含 |
|---|---|
| `control_plane` | 控制面服务器 |
| `operator_hosts` | 主控机 |
| `ubuntu_nodes` | Ubuntu 受管节点 |
| `mac_nodes` | macOS 节点 |
| `windows_nodes` | Windows 节点 |

## Tailnet DNS 命名

格式：`<node-name>.tailnet.<domain>`

示例：`ubuntu-master.tailnet.<SERVER_IP_DASHED>.sslip.io`

## 一致性要求

同一节点的名称在以下位置必须一致：
1. Headscale `given_name`
2. Ansible inventory `hosts.yml`
3. Ansible `host_vars/<name>.yml` 中的 `node_name`
4. 主控机 `~/.ssh/config` 中的 `Host` 别名
