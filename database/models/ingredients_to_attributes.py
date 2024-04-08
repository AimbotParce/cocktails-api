import secrets
from datetime import datetime
from typing import TypedDict

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text

from ..databases import database

IngredientToAttribute = Table(
    "ingredients_to_attributes",
    database.base.metadata,
    Column("ingredient_id", Integer, ForeignKey("ingredients.id"), primary_key=True, index=True),
    Column("attribute_id", Integer, ForeignKey("ingredient_attributes.id"), primary_key=True, index=True),
    Column("creation_datetime", DateTime, default=datetime.now),
)
