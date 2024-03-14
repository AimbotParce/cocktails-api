import secrets
from datetime import datetime
from typing import TypedDict

from sqlalchemy import Column, DateTime, Integer, String, Text

from ..databases import database


class Ingredient(database.base):
    "Ingredient model"
    __bind_key__ = database.bind_key
    __tablename__ = "ingredients"
    DATABASE = database

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    creation_datetime = Column(DateTime, default=datetime.now)
    image_uuid = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    name = Column(String(255), nullable=False, unique=True)
    type_id = Column(Integer, nullable=False)

    def __init__(self, name: str, type_id: int, image_uuid: str = None, description: str = None):
        self.name = name
        self.type_id = type_id
        self.image_uuid = image_uuid
        self.description = description

    def to_dict(self) -> "IngredientJSON":
        return {
            "id": self.id,
            "creation_datetime": self.creation_datetime,
            "image": self.image_uuid,
            "description": self.description,
            "name": self.name,
            "type_id": self.type_id,
        }


class IngredientJSON(TypedDict):
    id: int
    creation_datetime: datetime
    image_uuid: str
    description: str
    name: str
    type_id: int
