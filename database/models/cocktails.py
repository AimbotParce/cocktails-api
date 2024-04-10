import secrets
from datetime import datetime
from typing import TypedDict

from sqlalchemy import ARRAY, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..databases import database
from .images import ImageJSON
from .ingredients import IngredientJSON


class Cocktail(database.base):
    "Cocktail model"
    __bind_key__ = database.bind_key
    __tablename__ = "cocktails"
    DATABASE = database

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    creation_datetime = Column(DateTime, default=datetime.now)
    instructions = Column(Text, default=str)
    image_uuid = Column(String(255), ForeignKey("images.uuid"), nullable=False)
    image = relationship("Image")
    name = Column(String(255), nullable=False)
    uuid = Column(String(255), nullable=False, unique=True, default=secrets.token_urlsafe)
    ingredients = relationship(
        "Ingredient",
        secondary="cocktails_to_ingredients",
        uselist=True,
        cascade="save-update, merge, refresh-expire, expunge",
        backref="cocktails",
    )

    def __init__(self, name: str, image_uuid: str = None, instructions: str = None):
        self.name = name
        self.image_uuid = image_uuid
        self.instructions = instructions

    def to_json(self) -> "CocktailJSON":
        return {
            "id": self.id,
            "creation_datetime": self.creation_datetime,
            "image": self.image.to_json(),
            "instructions": self.instructions,
            "name": self.name,
            "uuid": self.uuid,
            "ingredients": list(map(lambda ing: ing.to_json(), self.ingredients)),
        }


class CocktailJSON(TypedDict):
    id: int
    creation_datetime: datetime
    image: ImageJSON
    instructions: str
    name: str
    uuid: str
    ingredients: list[IngredientJSON]
