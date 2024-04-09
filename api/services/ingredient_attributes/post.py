import flask
from database.managers import IngredientManager

from ... import app
from ...serializers import Err, Ok, make_response


@app.post("/ingredient_attributes")
@make_response
def post_ingredient_attribute():
    if not "name" in flask.request.json:
        return Err("Missing ingredient attribute name")
    name = flask.request.json["name"]
    description = flask.request.json.get("description", None)

    with IngredientManager() as manager:
        attribute = manager.add_ingredient_attribute(name=name, description=description)
    return Ok(attribute)
