# 成语搜索项目

这是一个成语搜索项目，支持两种语言实现：Python版本和Node.js版本。

## 项目结构

```
nsh_chengyu/
├── .github/
│   └── workflows/
│       └── auto.yml          # GitHub Actions自动构建配置
├── python/                     # Python版本
│   ├── app.py                  # 应用入口
│   ├── config.py               # 配置文件
│   ├── db.py                   # 数据库操作
│   ├── search.py               # 搜索功能
│   ├── requirements.txt        # 依赖管理
│   ├── migrate_to_sqlite.py    # 数据库迁移
│   ├── create_inverted_index.py # 创建倒排索引
│   ├── idiom.json              # 成语数据
│   ├── idioms.db               # SQLite数据库
│   ├── data/                   # 数据文件夹
│   └── templates/              # 模板文件夹
├── nodejs/                     # Node.js版本
│   ├── app.js                  # 应用入口
│   ├── package.json            # 依赖管理
│   ├── config/                 # 配置文件夹
│   ├── controllers/            # 控制器文件夹
│   ├── models/                 # 模型文件夹
│   ├── routes/                 # 路由文件夹
│   ├── services/               # 服务文件夹
│   ├── utils/                  # 工具函数文件夹
│   ├── templates/              # 模板文件夹
│   ├── Dockerfile              # Docker构建文件
│   ├── docker-compose.yml      # Docker Compose配置
│   └── README.md               # Node.js版本说明文档
└── README.md                   # 项目根目录说明文档
```

## 功能说明

两个版本都实现了以下功能：

1. **成语搜索**：根据拼音、声母、韵母等条件搜索成语，支持位置条件搜索，使用倒排索引提高搜索性能
2. **成语添加**：用户可以添加新成语，需要审核
3. **成语审核**：管理员可以审核用户添加的成语，决定是否通过
4. **成语详情API**：提供RESTful API接口，获取成语详情

## 使用说明

### Python版本

1. 进入Python版本文件夹：
   ```bash
   cd python
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 启动应用：
   ```bash
   python app.py
   ```

### Node.js版本

1. 进入Node.js版本文件夹：
   ```bash
   cd nodejs
   ```

2. 安装依赖：
   ```bash
   npm install
   ```

3. 启动应用：
   ```bash
   npm start
   ```

### Docker部署（Node.js版本）

1. 进入Node.js版本文件夹：
   ```bash
   cd nodejs
   ```

2. 构建Docker镜像：
   ```bash
   docker build -t mdespot/nsh-chengyu:latest .
   ```

3. 运行Docker容器：
   ```bash
   docker-compose up -d
   ```

## 访问应用

- 应用地址：http://localhost:8666
- 审核页面：http://localhost:8666/review
- API接口：http://localhost:8666/api/idiom/:word

## GitHub Actions自动构建

项目配置了GitHub Actions自动构建，当代码推送到`main`或`master`分支时，会自动构建Docker镜像并推送到Docker Hub。

也可以在GitHub仓库的Actions页面手动触发构建。