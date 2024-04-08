from ..exceptions import *
from ..models import Cocktail, CocktailToIngredient, Ingredient
from . import Manager


class CocktailManager(Manager):
    def get_cocktail(self, uuid: str):
        cocktail = self.session.query(Cocktail).filter(Cocktail.uuid == uuid).first()
        if not cocktail:
            raise NotFound()
        return cocktail.to_json()

    def get_cocktails(self, limit: int = None, offset: int = 0):
        cocktails = self.session.query(Cocktail).order_by(Cocktail.name)
        if limit:
            cocktails = cocktails.limit(limit)
        cocktails = cocktails.offset(offset)
        return list(map(lambda cocktail: cocktail.to_json(), cocktails.all()))

    def add_cocktail(
        self, name: str, ingredient_ids: list[int] = [], image_uuid: str = None, instructions: str = None
    ):
        if image_uuid is None:
            image_uuid = DEFAULT_COCKTAIL_IMAGE_UUID

        for ingredient_id in ingredient_ids:
            ingredient = self.session.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
            if not ingredient:
                raise NotFound()

        cocktail = Cocktail(name=name, image_uuid=image_uuid, instructions=instructions)
        self.session.add(cocktail)
        self.session.commit()
        cocktail_id = cocktail.id
        self.session.close()
        self.session = self.DATABASE.session()
        cocktail2 = self.session.query(Cocktail).filter(Cocktail.id == cocktail_id).first()

        for ingredient_id in ingredient_ids:
            ingredient = self.session.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
            if not ingredient:
                raise NotFound()
            cocktail_to_ingredient = CocktailToIngredient(cocktail_id=cocktail_id, ingredient_id=ingredient_id)
            self.session.add(cocktail_to_ingredient)

        return cocktail2.to_json()


from . import DEFAULT_COCKTAIL_IMAGE_UUID
