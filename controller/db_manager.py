from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from model.data_model import Base

DB_NAME = "mytestdb2"
_CONNECTION_STRING = "postgres+psycopg2://{0}:{1}@{2}/%s" % DB_NAME

class DatabaseManager(object):
    __instance = None

    def __new__(cls):
        if DatabaseManager.__instance is None:
            DatabaseManager.__instance = object.__new__(cls)
            DatabaseManager.__instance.engine = create_engine(_CONNECTION_STRING.format("postgres", "example", "172.17.0.1:5433"), echo=True)
            
            # Create a configured "Session" class
            sm = sessionmaker(bind=DatabaseManager.__instance.engine, autoflush=True, autocommit=False)
            DatabaseManager.__instance.session = sm()
        return DatabaseManager.__instance

    def __getattr__(self, name):
        return getattr(self.__instance, name)

    def create_structure(self):
        Base.metadata.create_all(self.engine)

    def drop_structure(self):
        Base.metadata.drop_all(self.engine)

    def execute(self, statement):
        with self.engine.connect() as cn:
            cn.execute(statement)
