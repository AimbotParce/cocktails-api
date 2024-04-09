from ..exceptions import *
from ..models import Cocktail, Ingredient, IngredientAttribute, IngredientToAttribute
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
        image_uuid: str = None,
        description: str = None,
    ):
        if image_uuid is None:
            image_uuid = DEFAULT_INGREDIENT_IMAGE_UUID

        attribute_ids = []
        for attribute in attributes:
            if isinstance(attribute, int):
                attribute = (
                    self.session.query(IngredientAttribute).filter(IngredientAttribute.id == attribute_id).first()
                )
                if not attribute:
                    raise NotFound()
            elif isinstance(attribute, dict):
                attribute = self.session.query(IngredientAttribute).filter(**attribute).all()
                if not len(attribute) == 1:
                    raise NotFound()
                attribute = attribute[0]
            else:
                raise ValueError("Invalid attribute type")
            attribute_ids.append(attribute.id)

        ingredient = Ingredient(name=name, image_uuid=image_uuid, description=description)
        self.session.add(ingredient)
        self.session.commit()
        ingredient_id = ingredient.id
        self.session.close()
        self.session = self.DATABASE.session()
        ingredient2 = self.session.query(Ingredient).filter(Ingredient.id == ingredient_id).first()

        for attribute_id in attribute_ids:
            attribute = self.session.query(IngredientAttribute).filter(IngredientAttribute.id == attribute_id).first()
            if not attribute:
                raise NotFound()
            ingredient_to_attribute = IngredientToAttribute(ingredient_id=ingredient_id, attribute_id=attribute_id)
            self.session.add(ingredient_to_attribute)

        return ingredient2.to_json()

    def add_ingredient_attribute(self, name: str, description: str = None):
        attribute = IngredientAttribute(name=name, description=description)
        self.session.add(attribute)
        self.session.commit()
        return attribute.to_json()


from . import DEFAULT_INGREDIENT_IMAGE_UUID
