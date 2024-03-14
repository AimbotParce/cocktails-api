import secrets
from datetime import datetime
from typing import TypedDict

from sqlalchemy import Column, DateTime, Integer, String, Text

from ..databases import database


class IngredientType(database.base):
    "Ingredient type model"
    __bind_key__ = database.bind_key
    __tablename__ = "ingredient_types"
    DATABASE = database

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    creation_datetime = Column(DateTime, default=datetime.now)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)

    def __init__(self, name: str, description: str = None):
        self.name = name
        self.description = description

    def to_dict(self) -> "IngredientTypeJSON":
        return {
            "id": self.id,
            "creation_datetime": self.creation_datetime,
            "name": self.name,
            "description": self.description,
        }


class IngredientTypeJSON(TypedDict):
    id: int
    creation_datetime: datetime
    name: str
    description: str
