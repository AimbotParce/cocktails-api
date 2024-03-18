import flask

from database.managers import CocktailManager

from .... import app
from ....serializers import BooleanField, Err, Ok, make_response


@app.get("/cocktails/<str:uuid>")
@make_response
def get_cocktail(uuid: str):
    with CocktailManager() as manager:
        cocktail = manager.get_cocktail(uuid=uuid)
    return Ok(cocktail)
