import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'c832ebc5c8f34a4bfab'
    DEBUG = False
    # API key to access food nutrition database
    USDA_API_KEY = os.environ.get("USDA_API_KEY")


class DevelopmentConfig(Config):
    ''' Development configurations '''
    DEBUG = True


class ProductionConfig(Config):
    ''' Production configurations '''
    pass


class TestingConfig(Config):
    ''' Testing configurations '''
    TESTING = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}