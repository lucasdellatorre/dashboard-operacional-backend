from app.infraestructure.utils.enviroment import databaseUrl, env
from app.infraestructure.utils.enviroment import pgUsername, pgPassword, pgInternalPort, pgDbName

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = databaseUrl.replace("postgres://", "postgresql+psycopg2://", 1)

class StagingConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = databaseUrl.replace("postgres://", "postgresql+psycopg2://", 1)

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = databaseUrl.replace("postgres://", "postgresql+psycopg2://", 1)

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TESTING = True
    
class LocalConfig(Config):
    DEBUG = True
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