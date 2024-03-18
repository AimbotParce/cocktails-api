import flask

from database.managers import CocktailManager

from ... import app
from ...serializers import Err, Ok, make_response


@app.put("/cocktails")
@make_response
def put_cocktail():
    if not "name" in flask.request.json:
        return Err("Missing cocktail name")
    name = flask.request.json["name"]
    ingredients = flask.request.json.get("ingredients", [])
    image_uuid = flask.request.json.get("image_uuid", None)
    instructions = flask.request.json.get("instructions", None)

    with CocktailManager() as manager:
        uuid = manager.add_cocktail(
            name=name, ingredients=ingredients, image_uuid=image_uuid, instructions=instructions
        )
    return Ok(uuid)
