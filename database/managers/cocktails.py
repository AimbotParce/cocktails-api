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

    def patch_cocktail(
        self,
        uuid: str,
        name: str = None,
        ingredients: list[int] | list[IngredientJSON] = None,
        image: str | ImageJSON = None,
        instructions: str = None,
    ):
        cocktail = self.session.query(Cocktail).filter(Cocktail.uuid == uuid).first()
        if not cocktail:
            raise NotFound("Cocktail uuid not found.")

        if name is not None:
            cocktail.name = name

        if instructions is not None:
            cocktail.instructions = instructions

        if image is not None:
            if isinstance(image, dict):
                image = self.session.query(Image).filter(Image.uuid == image["uuid"]).first()
            elif isinstance(image, str):
                image = self.session.query(Image).filter(Image.uuid == image).first()
            if not image:
                raise NotFound("Image not found.")

            cocktail.image = image

        if ingredients is not None:
            cocktail.ingredients = []
            for ingredient in ingredients:
                ingredient_instance = None
                if isinstance(ingredient, int):
                    ingredient_instance = self.session.query(Ingredient).filter(Ingredient.id == ingredient).first()
                elif isinstance(ingredient, dict):
                    ingredient_instance = (
                        self.session.query(Ingredient).filter(Ingredient.id == ingredient["id"]).first()
                    )
                if not ingredient_instance:
                    raise NotFound("One of the ingredients was not found.")
                cocktail.ingredients.append(ingredient_instance)

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
