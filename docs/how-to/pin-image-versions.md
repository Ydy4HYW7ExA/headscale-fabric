# Pin image versions

## 为什么要固定

Docker tag（如 `latest`、`0.23`）可能在不同时间拉取到不同镜像。固定 digest 确保每次部署完全一致。

## 当前固定方式

在 `group_vars/all.yml` 中用 `@sha256:` 格式固定：

```yaml
headscale_image: headscale/headscale@sha256:51b1b9182bb...
caddy_image: caddy@sha256:1e40b251ca...
```

## 更新流程

### 1. 查看最新 digest

```bash
docker pull headscale/headscale:latest
docker inspect headscale/headscale:latest --format '{{index .RepoDigests 0}}'
```

### 2. 更新 group_vars

将新 digest 写入 `scripts/ansible/inventories/production/group_vars/all.yml`。

### 3. 部署

```bash
python3 main/fabricctl/cli.py deploy
```

### 4. 验证

```bash
ssh root@<SERVER_IP> "docker images --digests | grep headscale"
```
