import flask
from database.exceptions import NotFound
from database.managers import IngredientManager

from .... import app
from ....serializers import BooleanField, Err, Ok, make_response


@app.patch("/ingredient_attributes/<name>")
@make_response
def patch_ingredient_attribute(name: str):
    new_name = flask.request.json.get("name")
    description = flask.request.json.get("description")
    with IngredientManager() as manager:
        try:
            attribute = manager.patch_ingredient_attribute(name=name, new_name=new_name, description=description)
        except NotFound:
            return Err(f"Attribute with name {name} not found")
    return Ok(attribute)
