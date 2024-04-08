import os

from ..databases import database


class Manager:
    DATABASE = database

    def __init__(self):
        self.session = self.DATABASE.session()

    def end(self):
        self.session.commit()
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end()

    def __del__(self):
        self.end()


from .attachments import AttachmentManager
from .defaults import DefaultsManager

with DefaultsManager() as defs:
    if not "DEFAULT_COCKTAIL_IMAGE_UUID" in defs:
        with AttachmentManager() as manager:
            DEFAULT_COCKTAIL_IMAGE_UUID = manager.add_image(
                "default-cocktail", open("/app/database/defaults/cocktail.jpg", "rb")
            )["uuid"]
    else:
        DEFAULT_COCKTAIL_IMAGE_UUID = defs.get("DEFAULT_COCKTAIL_IMAGE_UUID")

with DefaultsManager() as defs:
    if not "DEFAULT_INGREDIENT_IMAGE_UUID" in defs:
        with AttachmentManager() as manager:
            DEFAULT_INGREDIENT_IMAGE_UUID = manager.add_image(
                "default-ingredient", open("/app/database/defaults/ingredient.jpg", "rb")
            )["uuid"]
    else:
        DEFAULT_INGREDIENT_IMAGE_UUID = defs.get("DEFAULT_INGREDIENT_IMAGE_UUID")

from .cocktails import CocktailManager
from .ingredients import IngredientManager

__all__ = ["Manager", "CocktailManager", "AttachmentManager", "IngredientManager"]
