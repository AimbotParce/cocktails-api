import flask
from database.managers import IngredientManager

from ... import app
from ...serializers import Err, Ok, make_response


@app.post("/ingredients")
@make_response
def post_ingredient():
    if not "name" in flask.request.json:
        return Err("Missing ingredient name")
    name = flask.request.json["name"]
    attributes = flask.request.json.get("attributes", [])
    image = flask.request.json.get("image", None)
    description = flask.request.json.get("description", None)

    with IngredientManager() as manager:
        print(image, flush=True)
        ingredient = manager.add_ingredient(name=name, attributes=attributes, image=image, description=description)
    return Ok(ingredient)
