from datetime import datetime
from typing import TypedDict

from sqlalchemy import ARRAY, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..databases import database
from .images import ImageJSON
from .ingredient_attributes import IngredientAttributeJSON


class Ingredient(database.base):
    "Ingredient model"
    __bind_key__ = database.bind_key
    __tablename__ = "ingredients"
    DATABASE = database

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    creation_datetime = Column(DateTime, default=datetime.now)
    image_uuid = Column(String(255), ForeignKey("images.uuid"), nullable=False)
    image = relationship("Image")
    description = Column(Text, default=str)
    name = Column(String(255), unique=True)
    attributes = relationship("IngredientAttribute", secondary="ingredients_to_attributes", uselist=True)

    def __init__(self, name: str, image_uuid: str = None, description: str = None):
        self.name = name
        self.image_uuid = image_uuid
        self.description = description

    def to_json(self) -> "IngredientJSON":
        return {
            "id": self.id,
            "creation_datetime": self.creation_datetime,
            "image": self.image.to_json(),
            "description": self.description,
            "name": self.name,
            "attributes": list(map(lambda att: att.to_json(), self.attributes)),
        }


class IngredientJSON(TypedDict):
    id: int
    creation_datetime: datetime
    image: ImageJSON
    description: str
    name: str
    attributes: list[IngredientAttributeJSON]
