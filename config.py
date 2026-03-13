import os
import secrets

# 应用配置
class Config:
    # 用于会话管理的密钥
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(16))
    
    # 数据库路径
    DB_PATH = os.getenv('DB_PATH', 'idioms.db')
    
    # 管理员密码
    SECRET_PASSWORD = os.getenv('SECRET_PASSWORD', 'lsz20100')
    
    # 日志配置
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # 应用端口
    PORT = int(os.getenv('PORT', 8666))
    
    # 调试模式
    DEBUG = os.environ.get('FLASK_ENV') != 'production'