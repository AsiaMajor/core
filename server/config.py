class Config(object):
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    ENV = 'production'
    IN_PROD = True
    BACKEND_URL = 'https://ceklar-prod.herokuapp.com'

class StagingConfig(Config):
    ENV = 'staging'
    DEBUG = True
    BACKEND_URL = 'https://ceklar-staging.herokuapp.com'

class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    TESTING = True
    BACKEND_URL = 'http://127.0.0.1:5000'