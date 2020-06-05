import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # flash需要设置密钥
    SECRET_KEY = os.urandom(24)
    # 
    UPLOAD_FOLDER = BASE_DIR + '/App/static/uploads'
    ALLOWED_EXTENSIONS = set(['webm'])


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True

    DATA_FOLDER  = BASE_DIR + '/App/static/data'
    # 模型文件夹
    MODEL_FOLDER = BASE_DIR + '/App/model'
    # 模型文件名
    MODEL_FILENAME = 'VGG16.ckpt'



class TestingConfig(Config):
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
