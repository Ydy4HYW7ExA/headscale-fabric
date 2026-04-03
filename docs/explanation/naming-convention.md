# Naming convention

## 格式

节点命名按 `<os>-<标识>` 格式：

| 格式 | 含义 | 示例 |
|---|---|---|
| `ubuntu-master` | 主控机（固定名称） | 唯一 |
| `ubuntu-0` | 控制面服务器（Headscale 所在机器） | 唯一 |
| `ubuntu-<N>` | Ubuntu 受管节点，N 从 1 开始 | `ubuntu-1`, `ubuntu-2` |
| `mac-<N>` | macOS 节点 | `mac-1`, `mac-2` |
| `win-<N>` | Windows 节点 | `win-1`, `win-2` |

## 命名位置

同一节点的名称出现在三个位置，必须保持一致：

1. **Headscale given_name** — `headscale nodes rename -i <ID> <name>`
2. **Ansible inventory** — `scripts/ansible/inventories/production/hosts.yml`
3. **SSH config 别名** — 主控机 `~/.ssh/config`

## 按 OS 分组

- 分组的目的是 Ansible playbook 可以按 OS 批量操作
- 同一 OS 下的节点共享 group_vars（如 `ubuntu_nodes`、`mac_nodes`、`windows_nodes`）
- 扩展时保持此规律：新加一种 OS 就新增一个 `<os>_nodes` 组
