# nsh_chengyu - 逆水寒成语查询工具

这是一个为《逆水寒》枫林解语活动设计的成语查询工具，支持根据拼音声母和韵母条件查询成语。

## 功能特点

- 根据拼音声母和韵母条件查询成语
- 支持精确位置查询（第几个字的声母或韵母）
- 成语权重机制，根据使用频率调整排序
- 添加新成语功能（需审核）
- 响应式Web界面，支持移动设备
- 缓存优化，提高查询性能

## 项目结构

- `app.py`: 主应用文件，包含所有后端逻辑
- `data/idiom.json`: 成语数据文件
- `data/pending_idiom.json`: 待审核成语文件
- `templates/`: HTML模板文件目录
  - `index.html`: 主界面
  - `review_login.html`: 审核登录界面
  - `review.html`: 成语审核界面
- `requirements.txt`: Python依赖文件
- `Dockerfile`: Docker镜像配置
- `docker-compose.yml`: Docker部署配置

## 安装和运行

### 方法1：直接运行

1. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

2. 设置环境变量（可选）：
   ```
   export SECRET_KEY="your_secret_key"
   export SECRET_PASSWORD="your_admin_password"
   ```

3. 运行应用：
   ```
   python app.py
   ```

4. 访问 `http://localhost:8666`

### 方法2：使用Docker

1. 构建并启动容器：
   ```
   docker-compose up -d
   ```

2. 访问 `http://localhost:8666`

## 使用说明

1. 在主界面输入声母和韵母条件进行查询
2. 点击"添加成语"可提交新成语（需管理员审核）
3. 管理员可通过 `/review` 路径审核新成语

## 安全性

- 管理员密码通过SHA256哈希比较验证
- 使用环境变量管理密钥和密码
- 审核功能具有会话保护

## 优化建议

1. 使用数据库替代JSON文件存储，提高并发性能
2. 添加成语释义和出处信息
3. 实现拼音模糊匹配功能
4. 增加用户收藏功能
5. 添加搜索历史记录
6. 添加应用性能监控工具，如Prometheus指标导出
7. 实现更完善的错误处理机制，为不同类型的异常提供更具体的错误页面或日志记录
8. 为代码添加更详细的注释，特别是拼音解析和权重更新逻辑