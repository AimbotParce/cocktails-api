from ..exceptions import *
from ..models import Cocktail, Image, Ingredient, IngredientAttribute
from ..models.images import ImageJSON
from ..models.ingredient_attributes import IngredientAttributeJSON
from . import Manager


class IngredientManager(Manager):
    def get_ingredient(self, name: str):
        ingredient = self.session.query(Ingredient).filter(Ingredient.name == name).first()
        if not ingredient:
            raise NotFound()
        return ingredient.to_json()

    def get_ingredients(self, limit: int = None, offset: int = 0):
        ingredients = self.session.query(Ingredient).order_by(Ingredient.name)
        if limit:
            ingredients = ingredients.limit(limit)
        ingredients = ingredients.offset(offset)

        return list(map(lambda ingredient: ingredient.to_json(), ingredients.all()))

    def get_attribute(self, name: str):
        attribute = self.session.query(IngredientAttribute).filter(IngredientAttribute.name == name).first()
        if not attribute:
            raise NotFound()
        return attribute.to_json()

    def get_attributes(self, limit: int = None, offset: int = 0):
        attributes = self.session.query(IngredientAttribute).order_by(IngredientAttribute.name)
        if limit:
            attributes = attributes.limit(limit)
        attributes = attributes.offset(offset)

        return list(map(lambda attributes: attributes.to_json(), attributes.all()))

    def add_ingredient(
        self,
        name: str,
        attributes: list[int] | list[IngredientAttributeJSON] = [],
        image: str | ImageJSON = None,
        description: str = None,
    ):
        if image is None:
            image = self.session.query(Image).filter(Image.uuid == DEFAULT_INGREDIENT_IMAGE_UUID).first()
        elif isinstance(image, dict):
            image = self.session.query(Image).filter(Image.uuid == image["uuid"]).first()
        elif isinstance(image, str):
            image = self.session.query(Image).filter(Image.uuid == image).first()
        if not image:
            raise NotFound()

        attribute_ids = []
        for attribute in attributes:
            if isinstance(attribute, int):
                attribute = self.session.query(IngredientAttribute).filter(IngredientAttribute.id == attribute).first()
            elif isinstance(attribute, dict):
                attribute = (
                    self.session.query(IngredientAttribute).filter(IngredientAttribute.id == attribute["id"]).first()
                )
            else:
                raise ValueError("Invalid attribute type")
            if not attribute:
                raise NotFound()
            attribute_ids.append(attribute.id)

        ingredient = Ingredient(name=name, description=description)
        self.session.add(ingredient)

        ingredient.image = image

        for attribute_id in attribute_ids:
            attribute = self.session.query(IngredientAttribute).filter(IngredientAttribute.id == attribute_id).first()
            if not attribute:
                raise NotFound()
            ingredient.attributes.append(attribute)

        return ingredient.to_json()

    def add_ingredient_attribute(self, name: str, description: str = None):
        attribute = IngredientAttribute(name=name, description=description)
        self.session.add(attribute)
        self.session.commit()
        return attribute.to_json()


from . import DEFAULT_INGREDIENT_IMAGE_UUID
