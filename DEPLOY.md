# 部署指南

## 使用 Docker Compose 部署

### 前提条件
- 安装 Docker 和 Docker Compose
- 确保 Docker 服务正在运行

### 步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/xztxy/nsh_chengyu2025.git
   cd nsh_chengyu2025
   ```

2. **配置环境变量**
   创建一个 `.env` 文件，添加以下内容：
   ```
   # 可选：设置自定义密钥
   SECRET_KEY=your_secret_key_here
   
   # 可选：设置管理员密码
   SECRET_PASSWORD=your_admin_password_here
   ```

3. **启动服务**
   ```bash
   docker-compose up -d
   ```

4. **验证部署**
   打开浏览器访问 `http://localhost:8666`，应该能看到成语搜索应用的界面。

### 管理命令

- **查看服务状态**：
  ```bash
  docker-compose ps
  ```

- **查看服务日志**：
  ```bash
  docker-compose logs -f
  ```

- **停止服务**：
  ```bash
  docker-compose down
  ```

- **重启服务**：
  ```bash
  docker-compose restart
  ```

## 环境变量说明

- `FLASK_ENV`：Flask 运行环境，默认为 production
- `PORT`：应用运行端口，默认为 8666
- `SECRET_KEY`：Flask 会话密钥，默认为随机生成
- `SECRET_PASSWORD`：管理员密码，默认为 lsz20100
- `DB_PATH`：数据库路径，默认为 idioms.db

## 注意事项

- 首次启动时，应用会自动创建数据库并初始化数据
- 数据会存储在 `nsh-chengyu-db` 卷中，确保数据持久化
- 应用使用非 root 用户运行，提高安全性
- 配置了健康检查，确保服务正常运行
