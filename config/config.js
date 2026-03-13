// 应用配置
module.exports = {
  // 用于会话管理的密钥
  SECRET_KEY: process.env.SECRET_KEY || 'default_secret_key',
  
  // 数据库路径
  DB_PATH: process.env.DB_PATH || './data/idioms.db',
  
  // 管理员密码
  SECRET_PASSWORD: process.env.SECRET_PASSWORD || 'lsz20100',
  
  // 日志配置
  LOG_LEVEL: process.env.LOG_LEVEL || 'info',
  
  // 应用端口
  PORT: process.env.PORT || 8666,
  
  // 调试模式
  DEBUG: process.env.NODE_ENV !== 'production'
};