import flask
from database.exceptions import NotFound
from database.managers import IngredientManager

from .... import app
from ....serializers import BooleanField, Err, Ok, make_response


@app.patch("/ingredients/<name>")
@make_response
def patch_ingredient(name: str):
    new_name = flask.request.json.get("name", None)
    attributes = flask.request.json.get("attributes", None)
    image = flask.request.json.get("image", None)
    description = flask.request.json.get("description", None)
    with IngredientManager() as manager:
        try:
            ingredient = manager.patch_ingredient(
                name=name, new_name=new_name, attributes=attributes, image=image, description=description
            )
        except NotFound:
            return Err(f"Ingredient with name {name} not found")
    return Ok(ingredient)
