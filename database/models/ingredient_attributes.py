import secrets
from datetime import datetime
from typing import TypedDict

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from ..databases import database


class IngredientAttribute(database.base):
    "Ingredient attribute model, such as alcoholic, non-alcoholic, etc."
    __bind_key__ = database.bind_key
    __tablename__ = "ingredient_attributes"
    DATABASE = database

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    creation_datetime = Column(DateTime, default=datetime.now)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=False, default=str)

    def __init__(self, name: str, description: str = None):
        self.name = name
        self.description = description

    def to_json(self) -> "IngredientAttributeJSON":
        return {
            "id": self.id,
            "creation_datetime": self.creation_datetime,
            "name": self.name,
            "description": self.description,
        }


class IngredientAttributeJSON(TypedDict):
    id: int
    creation_datetime: datetime
    name: str
    description: str
