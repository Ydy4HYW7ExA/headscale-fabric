# Repository layout

```
headscale-fabric/
├── assets/
│   ├── templates/           # Jinja2 配置模板（唯一模板来源）
│   │   ├── headscale/       # config.yaml, docker-compose.yml, policy.json, snapshot.sh
│   │   ├── caddy/           # Caddyfile
│   │   ├── downloads/       # 门户页面和安装脚本
│   │   ├── ssh/             # SSH config 模板
│   │   └── watchdog/         # 看门狗脚本（Linux/macOS/Windows）
│   └── examples/            # 示例文件
├── docs/                    # Diataxis 结构文档
│   ├── tutorials/           # 入门教程（bootstrap、add node）
│   ├── how-to/              # 操作指南（backup、rename、rotate keys）
│   ├── explanation/         # 概念说明（architecture、naming、trust-vs-acl）
│   └── reference/           # 参考手册（CLI、inventory、runbook）
├── scripts/
│   ├── ansible/
│   │   ├── ansible.cfg
│   │   ├── inventories/     # production + staging inventory
│   │   ├── playbooks/       # 部署、备份、策略、节点管理
│   │   └── roles/            # Ansible roles
│   ├── bootstrap/           # 初始化脚本
│   └── helpers/             # 轻量渲染辅助（render-policy, render-downloads）
├── main/
│   └── fabricctl/           # 主控 CLI（deploy, backup, apply-policy, status）
├── tools/
│   └── opsctl/              # 运维 CLI（status, keys, policy, portal, backup）
│       └── main/opsctl/
├── Makefile
├── README.md
└── .gitignore
```

## 职责边界

| 目录 | 职责 | 谁调用 |
|---|---|---|
| `assets/templates/` | 配置模板 | Ansible playbook 引用 |
| `scripts/ansible/` | 部署编排 | fabricctl 或直接 ansible-playbook |
| `scripts/helpers/` | 本地渲染预览 | 开发时手动 |
| `main/fabricctl/` | 主控操作入口 | 用户直接调用 |
| `tools/opsctl/` | 运维只读查看 | 用户直接调用 |
