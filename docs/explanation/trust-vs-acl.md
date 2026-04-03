# Trust vs ACL

本仓库明确区分两类控制平面，它们互不替代。

## Headscale ACL（网络层）

**管什么**：节点之间在 tailnet 上能否建立网络连接。

- ACL 策略存储在 Headscale 数据库中（`policy: mode: database`），通过 `headscale policy set` 命令下发。
- 仓库模板：`assets/templates/headscale/policy.json.j2`。
- 应用流程：将策略草案放到服务器 `/opt/headscale/planned/policy.next.json`，然后执行 `fabricctl apply-policy`。
- 渲染预览：`python3 scripts/helpers/render-policy.py` 可从 inventory 和服务器快照生成策略 JSON。

当前策略要点：
- `ubuntu-master` 和 `ubuntu-1` 可访问所有节点的所有端口。
- `mac-1` 可访问 ubuntu 节点的 SSH 端口（22）和 `win-1` 的所有端口。
- `win-1` 可访问 ubuntu 节点的 SSH 端口（22）和 `mac-1` 的所有端口。
- ACL 只管"能不能建立连接"，不管"连接后有没有权限"。

## SSH 信任关系（认证层）

**管什么**：谁可以免密登录谁。

- 通过 SSH 公钥分发维护（`~/.ssh/authorized_keys`）。
- 仓库模板：`assets/templates/ssh/ssh_config_ubuntu.j2`、`ssh_config_mac.j2`。
- `ubuntu-master` 的公钥已分发到所有节点，实现单向免密。
- 其他节点之间没有交叉免密关系。

## 两者的关系

- ACL 允许 ≠ SSH 免密
- ACL 不允许 → SSH 一定不通（网络层就被拦了）
- ACL 允许 + 没有公钥 → SSH 需要密码
- ACL 允许 + 有公钥 → SSH 免密

**设计原则**：
1. ACL 尽量宽松（同 tailnet 内默认互通），安全边界交给 SSH 层。
2. SSH 免密严格单向——只有主控机 → 受管节点，不反过来。
3. `mac-1` 和 `win-1` 可以网络互联（ACL 允许），但没有交叉 SSH 免密。
4. 新增节点时，先在 ACL 中授权网络访问，再按需分发 SSH 公钥。
