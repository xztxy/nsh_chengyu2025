# 第一阶段：构建依赖
FROM node:16-slim AS builder

# 设置工作目录
WORKDIR /app

# 复制package.json和package-lock.json
COPY package*.json ./

# 安装依赖
RUN npm install

# 第二阶段：运行环境
FROM node:16-slim

# 设置工作目录
WORKDIR /app

# 创建非root用户和组
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# 安装运行依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 从构建阶段复制依赖
COPY --from=builder /app/node_modules /app/node_modules

# 复制项目代码
COPY . .

# 确保数据目录存在
RUN mkdir -p /app/data

# 更改文件所有者
RUN chown -R appuser:appgroup /app

# 切换到非root用户
USER appuser

# 暴露端口
EXPOSE 8666

# 设置环境变量
ENV NODE_ENV=production
ENV PORT=8666
ENV DB_PATH=/app/data/idioms.db

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8666/ || exit 1

# 启动应用
CMD ["node", "app.js"]