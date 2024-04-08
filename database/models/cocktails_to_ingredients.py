import secrets
from datetime import datetime
from typing import TypedDict

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from ..databases import database


class CocktailToIngredient(database.base):
    "Cocktail 2 ingredient model."
    __bind_key__ = database.bind_key
    __tablename__ = "cocktails_to_ingredients"
    DATABASE = database

    cocktail_id = Column(Integer, ForeignKey("cocktails.id"), primary_key=True, index=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), primary_key=True, index=True)
    creation_datetime = Column(DateTime, default=datetime.now)

    def __init__(self, cocktail_id: int, ingredient_id: int):
        self.cocktail_id = cocktail_id
        self.ingredient_id = ingredient_id

    def to_json(self) -> "CocktailToIngredientJSON":
        return {
            "cocktail_id": self.cocktail_id,
            "ingredient_id": self.ingredient_id,
            "creation_datetime": self.creation_datetime,
        }


class CocktailToIngredientJSON(TypedDict):
    ingredient_id: int
    cocktail_id: int
    creation_datetime: datetime
