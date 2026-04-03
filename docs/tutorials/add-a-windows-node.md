# Add a Windows node

将一台 Windows 机器接入 tailnet。

## 步骤

### 1. 安装 Tailscale

从官网下载并安装 Tailscale MSI：

```
https://pkgs.tailscale.com/stable/tailscale-setup-latest-amd64.msi
```

### 2. 访问门户

在 Windows 浏览器中打开：

```
https://headscale.<SERVER_IP_DASHED>.sslip.io/downloads/windows.html
```

页面提供两步操作：下载官方 MSI（如已安装可跳过）+ 下载接入脚本。

### 3. 运行接入脚本

下载 `join-windows.cmd` 后，右键选择"以管理员身份运行"。脚本会：
- 检查 Tailscale 是否已安装（未安装会提示先安装 MSI）
- 使用 preauth key 自动加入 tailnet

### 4. 验证

在 CMD 中运行：

```cmd
tailscale status
```

### 5. 在主控机确认

```bash
opsctl status
```

### 6. 命名

如果自动名称不对，通过 headscale 重命名为 `win-<N>`。

### 7. 开启远程桌面（可选）

如需从主控机远程桌面连接 Windows：

```cmd
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f
netsh advfirewall firewall add rule name="RDP-3389" dir=in action=allow protocol=TCP localport=3389
```

## 看门狗守护

接入脚本会自动部署看门狗（watchdog），通过 Task Scheduler 每分钟检查 tailscale 是否正常在线，掉线时自动执行 `tailscale up` 重新连接。

管理方式：

- **禁用看门狗**：`echo false > C:\headscale-fabric\watchdog.enabled`
- **启用看门狗**：`echo true > C:\headscale-fabric\watchdog.enabled`
- **移除看门狗**：`schtasks /delete /tn "HeadscaleFabricWatchdog" /f`

日志位于 `C:\headscale-fabric\watchdog.log`。
