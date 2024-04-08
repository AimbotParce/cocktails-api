from ..exceptions import *
from ..models import Cocktail, Ingredient, IngredientAttribute
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

    def add_cocktail(self, name: str, ingredients: list = [], image_uuid: str = None, instructions: str = None):
        if image_uuid is None:
            image_uuid = DEFAULT_COCKTAIL_IMAGE_UUID
        cocktail = Cocktail(name=name, ingredients=ingredients, image_uuid=image_uuid, instructions=instructions)
        self.session.add(cocktail)
        self.session.commit()
        return cocktail.to_json()


from . import DEFAULT_COCKTAIL_IMAGE_UUID
