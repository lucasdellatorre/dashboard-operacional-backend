import dotenv
import os

class ENVIRONMENT:
    def __init__(self):
        dotenv.load_dotenv()
        self.host = os.getenv("DASHBOARDOP_HOST")
        self.port = os.getenv("DASHBOARDOP_PORT")
        self.prefix = os.getenv("DASHBOARDOP_API_PREFIX")
        self.database_url = os.getenv("DATABASE_URL")
        self.env = os.getenv("DASHBOARDOP_ENV")
        self.pg_internal_host = os.getenv("POSTGRESQL_INTERNAL_HOST")
        self.pg_internal_port = os.getenv("POSTGRESQL_INTERNAL_PORT")
        self.pg_username = os.getenv("POSTGRESQL_USERNAME")
        self.pg_password = os.getenv("POSTGRESQL_PASSWORD")
        self.pg_db = os.getenv("POSTGRESQL_DB")
        self.redis_host = os.getenv("REDIS_HOST")
        self.redis_port = os.getenv("REDIS_PORT", 6379)
        self.redis_cloud = os.getenv("REDISCLOUD_URL")

    def get_instance(self):
        if not hasattr(self, "_instance"):
            self._instance = ENVIRONMENT()
        return self._instance

    def getHost(self):
        return self.host

    def getPort(self):
        return self.port

    def getPrefix(self):
        return self.prefix

    def getDatabaseUrl(self):
        return self.database_url
    
    def getEnv(self):
        return self.env
    
    def getPgInternalHost(self):
        return self.pg_internal_host
    
    def getPgInternalPort(self):
        return self.pg_internal_port
    
    def getPgUsername(self):
        return self.pg_username
    
    def getPgPassword(self):
        return self.pg_password
    
    def getPgDbName(self):
        return self.pg_db
    
    def getRedisHost(self):
        return self.redis_host

    def getRedisPort(self):
        return self.redis_port    
    
    def getRedisCloud(self):
        return self.redis_cloud

host = ENVIRONMENT().get_instance().getHost()
port = ENVIRONMENT().get_instance().getPort()
prefix = ENVIRONMENT().get_instance().getPrefix()
databaseUrl = ENVIRONMENT().get_instance().getDatabaseUrl()
env = ENVIRONMENT().get_instance().getEnv()
pgInternalHost = ENVIRONMENT().get_instance().getPgInternalHost()
pgInternalPort =ENVIRONMENT().get_instance().getPgInternalPort()
pgUsername = ENVIRONMENT().get_instance().getPgUsername()
pgPassword = ENVIRONMENT().get_instance().getPgPassword()
pgDbName = ENVIRONMENT().get_instance().getPgDbName()