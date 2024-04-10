import flask
from database.exceptions import NotFound
from database.managers import CocktailManager

from .... import app
from ....serializers import BooleanField, Err, Ok, make_response


@app.delete("/cocktails/<uuid>")
@make_response
def delete_cocktail(uuid: str):
    with CocktailManager() as manager:
        try:
            manager.delete_cocktail(uuid=uuid)
        except NotFound:
            return Err(f"Cocktail with UUID {uuid} not found")
    return Ok()
