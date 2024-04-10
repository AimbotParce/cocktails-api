import flask
from database.exceptions import NotFound
from database.managers import IngredientManager

from .... import app
from ....serializers import BooleanField, Err, Ok, make_response


@app.get("/ingredient_attributes/<name>")
@make_response
def delete_ingredient_attribute(name: str):
    with IngredientManager() as manager:
        try:
            manager.delete_attribute(name=name)
        except NotFound:
            return Err(f"Attribute with name {name} not found")
    return Ok()
