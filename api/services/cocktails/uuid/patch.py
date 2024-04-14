import flask
from database.exceptions import NotFound
from database.managers import CocktailManager

from .... import app
from ....serializers import BooleanField, Err, Ok, make_response


@app.patch("/cocktails/<uuid>")
@make_response
def patch_cocktail(uuid: str):
    name = flask.request.json.get("name", None)
    ingredients = flask.request.json.get("ingredients", None)
    image = flask.request.json.get("image", None)
    instructions = flask.request.json.get("instructions", None)
    with CocktailManager() as manager:
        try:
            cocktail = manager.patch_cocktail(
                uuid=uuid, name=name, ingredients=ingredients, image=image, instructions=instructions
            )
        except NotFound as e:
            return Err(str(e))
    return Ok(cocktail)
