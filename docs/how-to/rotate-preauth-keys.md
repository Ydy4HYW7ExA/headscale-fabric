# Rotate preauth keys

## 什么时候需要

- 现有 key 即将过期
- 怀疑 key 泄露
- 定期安全轮换

## 自动轮换（推荐）

```bash
ansible-playbook -i scripts/ansible/inventories/production/hosts.yml \
  scripts/ansible/playbooks/rotate-keys.yml
```

这会：过期所有现有 reusable key → 创建新的 24h reusable key → 更新快照。

## 手动轮换

```bash
# 列出现有 key
ssh root@<SERVER_IP> "docker exec headscale headscale preauthkeys list -u default"

# 过期指定 key
ssh root@<SERVER_IP> "docker exec headscale headscale preauthkeys expire --key <KEY> -u default"

# 创建新 key
ssh root@<SERVER_IP> "docker exec headscale headscale preauthkeys create -u default --reusable --expiration 24h"
```

## 注意

轮换 key 后，门户脚本中硬编码的 key 需要同步更新。重新运行 `deploy-downloads.yml` 即可。
