import flask
from database.managers import CocktailManager

from ... import app
from ...serializers import Err, Ok, make_response


@app.post("/cocktails")
@make_response
def post_cocktail():
    if not "name" in flask.request.json:
        return Err("Missing cocktail name")
    name = flask.request.json["name"]
    ingredient_ids = flask.request.json.get("ingredient_ids", [])
    image_uuid = flask.request.json.get("image_uuid", None)
    instructions = flask.request.json.get("instructions", None)

    with CocktailManager() as manager:
        cocktail = manager.add_cocktail(
            name=name, ingredient_ids=ingredient_ids, image_uuid=image_uuid, instructions=instructions
        )
    return Ok(cocktail)
