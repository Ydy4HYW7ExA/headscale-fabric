# Bootstrap a new server

从零初始化一台公网服务器并部署 Headscale 控制面。

## 前提

- 一台干净的 Ubuntu 服务器，有公网 IP
- 主控机已安装 Ansible（`scripts/bootstrap/install-ansible.sh`）
- 已将服务器信息更新到 inventory `hosts.yml` 的 `control_plane` 组

## 步骤

### 1. 更新 inventory

编辑 `scripts/ansible/inventories/production/hosts.yml`，将新服务器 IP 填入 `ubuntu-0`：

```yaml
control_plane:
  hosts:
    ubuntu-0:
      ansible_host: <新服务器IP>
      ansible_user: root
```

### 2. 更新 group_vars

确认 `group_vars/all.yml` 中的域名和镜像 digest 正确。

### 3. 运行 bootstrap playbook

```bash
cd ~/work/repositories/headscale-fabric
ansible-playbook -i scripts/ansible/inventories/production/hosts.yml \
  scripts/ansible/playbooks/bootstrap-server.yml
```

这会自动完成：安装 Docker、创建目录结构、下发模板、启动容器、创建默认用户、生成 preauth key。

### 4. 验证

```bash
python3 main/fabricctl/cli.py status
```

应该能看到控制面容器在线、节点列表为空（新服务器）。

### 5. 部署门户

```bash
ansible-playbook -i scripts/ansible/inventories/production/hosts.yml \
  scripts/ansible/playbooks/deploy-downloads.yml
```

之后可以通过 `https://headscale.<SERVER_IP_DASHED>.sslip.io/downloads/` 访问门户。
