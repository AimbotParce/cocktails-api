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
    attribute_ids = flask.request.json.get("attribute_ids", [])
    image_uuid = flask.request.json.get("image_uuid", None)
    description = flask.request.json.get("description", None)

    with IngredientManager() as manager:
        ingredient = manager.add_ingredient(
            name=name, attribute_ids=attribute_ids, image_uuid=image_uuid, description=description
        )
    return Ok(ingredient)
