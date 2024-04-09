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
    ingredients = flask.request.json.get("ingredients", [])
    image = flask.request.json.get("image", None)
    instructions = flask.request.json.get("instructions", None)

    with CocktailManager() as manager:
        cocktail = manager.add_cocktail(name=name, ingredients=ingredients, image=image, instructions=instructions)
    return Ok(cocktail)
