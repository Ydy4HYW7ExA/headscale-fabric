# Add a macOS node

将一台 Mac 接入 tailnet。

## 步骤

### 1. 安装 tailscale

在 Mac 上执行门户一键脚本：

```bash
curl -fsSL https://headscale.<SERVER_IP_DASHED>.sslip.io/downloads/install-mac.sh | bash
```

或者手动安装：
- 从 [tailscale.com](https://tailscale.com/download) 下载 macOS 客户端
- 安装后在终端执行 `tailscale up --login-server https://headscale.<SERVER_IP_DASHED>.sslip.io --authkey <KEY>`

### 2. 验证连接

```bash
tailscale status
```

应看到其他节点列表。

### 3. 在主控机确认

```bash
opsctl status
```

新 Mac 节点应出现在 Control Plane 和 Local View 中。

### 4. 命名

如果自动名称不对，在主控机通过 headscale 重命名：

```bash
ssh root@<SERVER_IP> "docker exec headscale headscale nodes rename -i <ID> mac-<N>"
```

### 5. SSH 配置

在主控机 `~/.ssh/config` 中添加别名，参考 `assets/templates/ssh/ssh_config_mac.j2`。

## 看门狗守护

一键安装脚本会自动部署看门狗（watchdog），每分钟通过 cron 检查 tailscale 是否正常在线，掉线时自动执行 `tailscale up` 重新连接。

管理方式：

- **禁用看门狗**：`echo false > /etc/headscale-fabric/watchdog.enabled`
- **启用看门狗**：`echo true > /etc/headscale-fabric/watchdog.enabled`
- **移除看门狗**：`crontab -l | grep -v headscale-watchdog | crontab -`

日志位于 `/var/log/headscale-watchdog.log`。
