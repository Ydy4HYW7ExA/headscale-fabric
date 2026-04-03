# Update ACL policy

## 流程

### 1. 编辑策略草案

在服务器上编辑 planned 草案：

```bash
ssh root@<SERVER_IP> "vim /opt/headscale/planned/policy.next.json"
```

或本地编辑模板 `assets/templates/headscale/policy.json.j2`，然后用 helper 渲染：

```bash
python3 scripts/helpers/render-policy.py > /tmp/policy.next.json
scp /tmp/policy.next.json root@<SERVER_IP>:/opt/headscale/planned/policy.next.json
```

### 2. 应用策略

```bash
python3 main/fabricctl/cli.py apply-policy
```

底层 playbook 会先验证草案语法，再应用，最后打印生效策略。

### 3. 验证

```bash
cd tools/opsctl/main && PYTHONPATH=. python3 opsctl/cli.py policy
```

### 当前策略结构

```json
{
  "hosts": { "节点名": "IP/32", ... },
  "acls": [
    { "action": "accept", "src": ["ubuntu-master", "ubuntu-1"], "dst": ["*:*"] },
    { "action": "accept", "src": ["mac-1"], "dst": ["ubuntu-master:22", ...] },
    ...
  ]
}
```

核心原则：ubuntu-master 和 ubuntu-1 可访问所有节点，mac/win 只能访问指定端口。详见 `docs/explanation/trust-vs-acl.md`。
