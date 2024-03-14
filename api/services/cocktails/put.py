import flask

from database.managers import CocktailManager

from ... import app
from ...serializers import Err, Ok, make_response


@app.put("/cocktails")
@make_response
def put_cocktail():
    cocktail = flask.request.json

    if not cocktail:
        return Err("No data provided")

    with CocktailManager() as manager:
        uuid = manager.add_cocktail(cocktail)
    return Ok(uuid)
