from app.infraestructure.utils.enviroment import databaseUrl, env
from app.infraestructure.utils.enviroment import pgUsername, pgPassword, pgInternalPort, pgDbName

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = databaseUrl
    

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    
class LocalConfig(Config):
    SQLALCHEMY_DATABASE_URI=f'postgresql+psycopg2://{pgUsername}:{pgPassword}@localhost:{pgInternalPort}/{pgDbName}'

class ConfigFactory():
    @staticmethod
    def get_config():
        if env == 'development':
            return DevelopmentConfig()
        elif env == 'staging':
            return StagingConfig()
        elif env == 'production':
            return ProductionConfig()
        elif env == 'testing':
            return TestingConfig()
        elif env == 'local':
            return LocalConfig()
        else:
            raise ValueError('invalid env value!')