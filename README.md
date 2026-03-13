# 成语搜索项目 (Node.js Express 版本)

## 项目功能

1. **成语搜索**：根据拼音、声母、韵母等条件搜索成语
2. **成语添加**：用户可以添加新成语，需要审核
3. **成语审核**：管理员可以审核用户添加的成语
4. **成语详情API**：提供成语详情的API接口

## 项目结构

```
├── app.js              # 应用入口
├── package.json        # 依赖管理
├── package-lock.json   # 依赖版本锁定
├── Dockerfile          # Docker构建文件
├── docker-compose.yml  # Docker Compose配置
├── config/             # 配置文件
│   └── config.js       # 应用配置
├── routes/             # 路由
│   ├── index.js        # 路由入口
│   ├── search.js       # 搜索相关路由
│   ├── add.js          # 添加成语路由
│   ├── review.js       # 审核相关路由
│   └── api.js          # API接口路由
├── controllers/        # 控制器
│   ├── searchController.js    # 搜索控制器
│   ├── addController.js       # 添加成语控制器
│   ├── reviewController.js    # 审核控制器
│   └── apiController.js       # API控制器
├── services/           # 服务
│   ├── searchService.js       # 搜索服务
│   ├── idiomService.js        # 成语服务
│   └── reviewService.js       # 审核服务
├── models/             # 数据模型
│   ├── idiom.js        # 成语模型
│   ├── pendingIdiom.js # 待审核成语模型
│   └── invertedIndex.js # 倒排索引模型
├── utils/              # 工具函数
│   ├── pinyinUtils.js  # 拼音处理工具
│   └── dbUtils.js      # 数据库工具
├── templates/          # 模板文件
│   ├── index.html      # 首页模板
│   ├── review_login.html # 审核登录模板
│   └── review.html     # 审核页面模板
└── data/               # 数据文件
    └── idioms.db       # SQLite数据库文件
```

## 技术栈

- **后端**：Node.js, Express
- **数据库**：SQLite
- **模板引擎**：EJS
- **部署**：Docker, Docker Compose

## 核心功能实现

### 1. 成语搜索

- 支持根据拼音、声母、韵母等条件搜索
- 支持位置条件搜索（每个字的位置可以设置不同的条件）
- 使用倒排索引提高搜索性能

### 2. 成语添加和审核

- 用户可以添加新成语，需要填写成语和拼音
- 管理员可以审核用户添加的成语，决定是否通过
- 审核通过的成语会添加到正式成语库

### 3. 成语详情API

- 提供RESTful API接口，获取成语详情
- 支持JSON格式返回数据

## 部署方式

### Docker构建和运行

1. 构建Docker镜像：
   ```bash
   docker build -t mdespot/nsh-chengyu:latest .
   ```

2. 运行Docker容器：
   ```bash
   docker-compose up -d
   ```

3. 访问应用：
   ```
   http://localhost:8666
   ```

## API文档

### 获取成语详情

- **URL**：`/api/idiom/:word`
- **Method**：GET
- **参数**：
  - `word`：成语
- **返回**：
  ```json
  {
    "success": true,
    "data": {
      "word": "成语",
      "pinyin": "chéng yǔ",
      "pinyin_r": "cheng yu",
      "derivation": "成语的来源",
      "example": "成语的例子",
      "explanation": "成语的解释",
      "abbreviation": "cy",
      "first": "c",
      "last": "u",
      "weight": 1
    }
  }
  ```