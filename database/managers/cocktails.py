from ..models import Cocktail, Ingredient, IngredientType
from . import Manager


class CocktailManager(Manager):
    def get_cocktails(self):
        cocktails = self.session.query(Cocktail).order_by(Cocktail.name).all()
        return list(map(lambda cocktail: cocktail.to_dict(), cocktails))

    def add_cocktail(self, name: str, ingredients: list = [], image_uuid: str = None, instructions: str = None):
        cocktail = Cocktail(name=name, ingredients=ingredients, image_uuid=image_uuid, instructions=instructions)
        self.session.add(cocktail)
        self.session.commit()
        return cocktail.uuid
