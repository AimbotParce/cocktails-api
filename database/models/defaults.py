from datetime import datetime
from typing import TypedDict

from sqlalchemy import Column, DateTime, Integer, String, Text

from ..databases import database


class DefaultValue(database.base):
    "Defaults Model"
    __bind_key__ = database.bind_key
    __tablename__ = "defaults"
    DATABASE = database

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    creation_datetime = Column(DateTime, default=datetime.now)
    key = Column(String(255), nullable=False, unique=True)
    value = Column(Text, nullable=True)

    def __init__(self, key: str, value: str = None):
        self.key = key
        self.value = value

    def to_json(self) -> "DefaultValueJSON":
        return {
            "id": self.id,
            "creation_datetime": self.creation_datetime,
            "key": self.key,
            "value": self.value,
        }


class DefaultValueJSON(TypedDict):
    id: int
    creation_datetime: datetime
    key: str
    value: str
