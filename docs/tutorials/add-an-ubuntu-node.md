# Add an Ubuntu node

将一台 Ubuntu 机器接入 tailnet。

## 方法一：门户一键脚本

在目标机器上执行：

```bash
curl -fsSL https://headscale.<SERVER_IP_DASHED>.sslip.io/downloads/install-linux.sh | bash
```

脚本会自动安装 tailscale 并使用预设的 preauth key 加入网络。

## 方法二：Ansible playbook

在主控机上执行：

1. 将新节点加入 inventory（`hosts.yml` 的 `ubuntu_nodes` 组）
2. 创建 `host_vars/<node-name>.yml`，设置 `node_name` 和 `node_role`
3. 运行：

```bash
ansible-playbook -i scripts/ansible/inventories/production/hosts.yml \
  scripts/ansible/playbooks/add-ubuntu-node.yml --limit <node-name>
```

## 加入后

- 在主控机运行 `opsctl status` 确认新节点出现
- 如需免密 SSH，运行 `sync-ubuntu-user-env.yml` 分发公钥
- 在 Headscale 中用 `headscale nodes rename` 确保命名符合 `ubuntu-<N>` 规范

## 看门狗守护

一键安装脚本会自动部署看门狗（watchdog），每分钟通过 cron 检查 tailscale 是否正常在线，掉线时自动执行 `tailscale up` 重新连接。

管理方式：

- **禁用看门狗**：`echo false > /etc/headscale-fabric/watchdog.enabled`
- **启用看门狗**：`echo true > /etc/headscale-fabric/watchdog.enabled`
- **移除看门狗**：`crontab -l | grep -v headscale-watchdog | crontab -`

日志位于 `/var/log/headscale-watchdog.log`。
