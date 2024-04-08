import secrets
from datetime import datetime
from typing import TypedDict

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text

from ..databases import database

"Cocktail 2 ingredient model."
CocktailToIngredient = Table(
    "cocktails_to_ingredients",
    database.base.metadata,
    Column("cocktail_id", Integer, ForeignKey("cocktails.id"), primary_key=True, index=True),
    Column("ingredient_id", Integer, ForeignKey("ingredients.id"), primary_key=True, index=True),
    Column("creation_datetime", DateTime, default=datetime.now),
)
