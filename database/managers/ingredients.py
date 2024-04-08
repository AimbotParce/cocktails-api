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
