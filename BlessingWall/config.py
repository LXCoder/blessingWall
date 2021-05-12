import redis

class Config(object):
    SECRET_KEY = "safdasjlkdmas"

    # 数据库
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1/db_blessing'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # # redis
    # REDIS_HOST = "127.0.0.1"
    # REDIS_PORT = 6379

    # # flask-session设置
    # SESSION_TYPE = "redis"
    # SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    # SESSION_USE_SIGNER = True   # 对cookie中的session_id进行隐藏处理
    # PERMANENT_SESSION_LIFETIME = 86400 # session数据的有效期，单位秒

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):

    pass

config_map = {
    "develop":DevelopmentConfig,
    "product":ProductionConfig
}