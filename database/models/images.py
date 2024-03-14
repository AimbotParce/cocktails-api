import secrets
from datetime import datetime
from typing import TypedDict

from sqlalchemy import ARRAY, BINARY, Column, DateTime, Integer, String, Text

from ..databases import database


class Image(database.base):
    "Image model"
    __bind_key__ = database.bind_key
    __tablename__ = "images"
    DATABASE = database

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    creation_datetime = Column(DateTime, default=datetime.now)
    uuid = Column(String(255), nullable=False, unique=True, default=secrets.token_urlsafe)
    name = Column(String(255), nullable=False)
    image = Column(BINARY, nullable=False)

    def __init__(self, name: str, image: bytes):
        self.name = name
        self.image = image
