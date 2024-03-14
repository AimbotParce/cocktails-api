import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


class Database:
    def __init__(self, url: str, bind_key: str = None):
        self.engine = create_engine(url)
        self.__sessionmaker = sessionmaker(bind=self.engine)
        self.__session = None
        self.bind_key = bind_key
        self.base = declarative_base()

    def session(self):
        if self.__session is None:
            self.__session = self.__sessionmaker()
        return self.__session


database = Database(os.environ.get("DATABASE_URL"), "default")
