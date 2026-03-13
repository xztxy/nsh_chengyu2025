# 使用Node.js官方镜像
FROM node:16

# 设置工作目录
WORKDIR /app

# 复制package.json和package-lock.json
COPY package*.json ./

# 安装依赖
RUN npm install --production

# 复制项目代码
COPY . .

# 确保数据目录存在
RUN mkdir -p /app/data

# 暴露端口
EXPOSE 8666

# 设置环境变量
ENV NODE_ENV=production
ENV PORT=8666
ENV DB_PATH=/app/data/idioms.db

# 启动应用
CMD ["node", "app.js"]