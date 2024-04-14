from .attachments.images.get import get_all_images
from .attachments.images.post import post_image
from .attachments.images.uuid.delete import delete_image
from .attachments.images.uuid.get import get_image
from .cocktails.get import get_all_cocktails
from .cocktails.post import post_cocktail
from .cocktails.uuid.delete import delete_cocktail
from .cocktails.uuid.get import get_cocktail
from .cocktails.uuid.patch import patch_cocktail
from .ingredient_attributes.get import get_all_ingredient_attributes
from .ingredient_attributes.name.delete import delete_ingredient_attribute
from .ingredient_attributes.name.get import get_ingredient_attribute
from .ingredient_attributes.name.patch import patch_ingredient_attribute
from .ingredient_attributes.post import post_ingredient_attribute
from .ingredients.get import get_all_ingredients
from .ingredients.name.delete import delete_ingredient
from .ingredients.name.get import get_ingredient
from .ingredients.name.patch import patch_ingredient
from .ingredients.post import post_ingredient

__all__ = [
    "get_all_images",
    "get_all_cocktails",
    "delete_ingredient",
    "delete_ingredient_attribute",
    "patch_ingredient_attribute",
    "patch_ingredient",
    "delete_cocktail",
    "get_cocktail",
    "delete_image",
    "post_cocktail",
    "post_image",
    "patch_cocktail",
    "get_image",
    "get_all_ingredient_attributes",
    "get_ingredient_attribute",
    "post_ingredient_attribute",
    "get_all_ingredients",
    "post_ingredient",
    "get_ingredient",
]
