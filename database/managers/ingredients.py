from ..exceptions import *
from ..models import Cocktail, Ingredient, IngredientAttribute
from . import Manager


class IngredientManager(Manager):
    def get_ingredients(self, limit: int = None, offset: int = 0):
        ingredients = self.session.query(Ingredient).order_by(Ingredient.name)
        if limit:
            ingredients = ingredients.limit(limit)
        ingredients = ingredients.offset(offset)

        return list(map(lambda ingredient: ingredient.to_json(), ingredients.all()))

    def add_ingredient(
        self, name: str, attribute_ids: list[int] = [], image_uuid: str = None, description: str = None
    ):
        if image_uuid is None:
            image_uuid = DEFAULT_INGREDIENT_IMAGE_UUID

        for attribute_id in attribute_ids:
            attribute = self.session.query(IngredientAttribute).filter(IngredientAttribute.id == attribute_id).first()
            if not attribute:
                raise NotFound()

        ingredient = Ingredient(name=name, attribute_ids=attribute_ids, image_uuid=image_uuid, description=description)
        self.session.add(ingredient)
        self.session.commit()
        return ingredient.to_json()


from . import DEFAULT_INGREDIENT_IMAGE_UUID
