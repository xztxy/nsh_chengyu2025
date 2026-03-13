# 第一阶段：构建依赖
FROM python:3.9-slim AS builder

# 设置工作目录
WORKDIR /app

# 安装构建依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements.txt并安装依赖
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

# 第二阶段：运行环境
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 创建非root用户和组
RUN addgroup --system appgroup && adduser --system --group appgroup --uid 1000

# 安装运行依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 从构建阶段复制依赖
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

# 复制项目代码
COPY . .

# 初始化数据库
RUN python migrate_to_sqlite.py && python create_inverted_index.py

# 更改文件所有者
RUN chown -R 1000:appgroup /app

# 切换到非root用户
USER 1000

# 暴露端口
EXPOSE 8666

# 设置环境变量
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=8666
ENV DB_PATH=idioms.db

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8666/ || exit 1

# 启动应用
CMD ["python", "app.py"]