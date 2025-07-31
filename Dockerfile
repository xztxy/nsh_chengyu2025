# 使用官方Python运行时作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 创建非root用户
RUN addgroup --system appgroup && adduser --system --group appgroup

# 复制requirements.txt并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 更改文件所有者
RUN chown -R appuser:appgroup /app

# 切换到非root用户
USER appuser

# 暴露端口
EXPOSE 8666

# 设置环境变量
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=8666

# 启动应用
CMD ["python", "app.py"]
