import secrets
from datetime import datetime
from typing import TypedDict

from sqlalchemy import ARRAY, Column, DateTime, Integer, String, Text

from ..databases import database


class Cocktail(database.base):
    "Cocktail model"
    __bind_key__ = database.bind_key
    __tablename__ = "cocktails"
    DATABASE = database

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    creation_datetime = Column(DateTime, default=datetime.now)
    instructions = Column(Text, nullable=True)
    image_uuid = Column(String(255), nullable=True)
    name = Column(String(255), nullable=False)
    uuid = Column(String(255), nullable=False, unique=True, default=secrets.token_urlsafe)
    ingredients = Column(ARRAY(Integer), default=list)

    def __init__(self, name: str, ingredients: list = [], image_uuid: str = None, instructions: str = None):
        self.name = name
        self.ingredients = ingredients
        self.image_uuid = image_uuid
        self.instructions = instructions

    def to_dict(self) -> "CocktailJSON":
        return {
            "id": self.id,
            "creation_datetime": self.creation_datetime,
            "image": self.image_uuid,
            "instructions": self.instructions,
            "name": self.name,
            "uuid": self.uuid,
            "ingredients": self.ingredients,
        }


class CocktailJSON(TypedDict):
    id: int
    creation_datetime: datetime
    image_uuid: str
    instructions: str
    name: str
    uuid: str
    ingredients: list[int]
