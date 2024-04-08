import secrets
from datetime import datetime
from typing import TypedDict

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from ..databases import database


class IngredientToAttribute(database.base):
    "Ingredient 2 attribute model."
    __bind_key__ = database.bind_key
    __tablename__ = "ingredients_to_attributes"
    DATABASE = database

    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), primary_key=True, index=True)
    attribute_id = Column(Integer, ForeignKey("ingredient_attributes.id"), primary_key=True, index=True)
    creation_datetime = Column(DateTime, default=datetime.now)

    def __init__(self, ingredient_id: int, attribute_id: int):
        self.ingredient_id = ingredient_id
        self.attribute_id = attribute_id

    def to_json(self) -> "IngredientToAttributeJSON":
        return {
            "ingredient_id": self.ingredient_id,
            "attribute_id": self.attribute_id,
            "creation_datetime": self.creation_datetime,
        }


class IngredientToAttributeJSON(TypedDict):
    ingredient_id: int
    attribute_id: int
    creation_datetime: datetime
