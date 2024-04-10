from ..exceptions import *
from ..models import Cocktail, CocktailToIngredient, Image, Ingredient
from ..models.images import ImageJSON
from ..models.ingredients import IngredientJSON
from . import Manager


class CocktailManager(Manager):
    def get_cocktail(self, uuid: str):
        cocktail = self.session.query(Cocktail).filter(Cocktail.uuid == uuid).first()
        if not cocktail:
            raise NotFound()
        return cocktail.to_json()

    def delete_cocktail(self, uuid: str):
        cocktail = self.session.query(Cocktail).filter(Cocktail.uuid == uuid).first()
        if not cocktail:
            raise NotFound()
        self.session.delete(cocktail)

    def get_cocktails(self, limit: int = None, offset: int = 0):
        cocktails = self.session.query(Cocktail).order_by(Cocktail.name)
        if limit:
            cocktails = cocktails.limit(limit)
        cocktails = cocktails.offset(offset)
        return list(map(lambda cocktail: cocktail.to_json(), cocktails.all()))

    def add_cocktail(
        self,
        name: str,
        ingredients: list[int] | list[IngredientJSON] = [],
        image: str | ImageJSON = None,
        instructions: str = None,
    ):
        if image is None:
            image = self.session.query(Image).filter(Image.uuid == DEFAULT_COCKTAIL_IMAGE_UUID).first()
        elif isinstance(image, dict):
            image = self.session.query(Image).filter(Image.uuid == image["uuid"]).first()
        elif isinstance(image, str):
            image = self.session.query(Image).filter(Image.uuid == image).first()

        if not image:
            raise NotFound()

        ingredient_ids = []
        for ingredient in ingredients:
            if isinstance(ingredient, int):
                ingredient = self.session.query(Ingredient).filter(Ingredient.id == ingredient).first()
            elif isinstance(ingredient, dict):
                ingredient = self.session.query(Ingredient).filter(Ingredient.id == ingredient["id"]).first()
            else:
                raise ValueError("Invalid ingredient type")
            if not ingredient:
                raise NotFound()
            ingredient_ids.append(ingredient.id)

        cocktail = Cocktail(name=name, instructions=instructions)
        self.session.add(cocktail)

        cocktail.image = image

        for ingredient_id in ingredient_ids:
            ingredient = self.session.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
            if not ingredient:
                raise NotFound()
            cocktail.ingredients.append(ingredient)

        return cocktail.to_json()


from . import DEFAULT_COCKTAIL_IMAGE_UUID
