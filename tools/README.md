# tools

运维工具集合。当前包含 `opsctl`。

## opsctl

运维只读 CLI，用于查看 tailnet 状态、preauth keys、ACL 策略、门户和备份。

### 使用

```bash
cd tools/opsctl/main
PYTHONPATH=. python3 opsctl/cli.py <command>
```

### 命令

| 命令 | 说明 |
|---|---|
| `status` | 主动采集全网状态（tailscale + headscale 控制面） |
| `status --passive` | 被动读取服务器快照 |
| `keys` | 列出预授权密钥 |
| `policy` | 显示当前 ACL 策略 |
| `portal` | 显示门户文件和 Caddy 状态 |
| `backup` | 列出远程备份和最新快照 |
