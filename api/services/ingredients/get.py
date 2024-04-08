import flask
from database.managers import IngredientManager

from ... import app
from ...serializers import BooleanField, Err, Ok, make_response


@app.get("/ingredients")
@make_response
def get_all_ingredients():
    limit = flask.request.args.get("limit", None, type=int)
    offset = flask.request.args.get("offset", 0, type=int)

    with IngredientManager() as manager:
        ingredients = manager.get_ingredients(limit=limit, offset=offset)
    return Ok(ingredients)
