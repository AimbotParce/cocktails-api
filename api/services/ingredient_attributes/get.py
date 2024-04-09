import flask
from database.managers import IngredientManager

from ... import app
from ...serializers import BooleanField, Err, Ok, make_response


@app.get("/ingredient_attributes")
@make_response
def get_all_ingredient_attributes():
    limit = flask.request.args.get("limit", None, type=int)
    offset = flask.request.args.get("offset", 0, type=int)

    with IngredientManager() as manager:
        attributes = manager.get_attributes(limit=limit, offset=offset)
    return Ok(attributes)
