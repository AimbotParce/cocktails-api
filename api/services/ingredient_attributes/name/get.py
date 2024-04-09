import flask
from database.exceptions import NotFound
from database.managers import IngredientManager

from .... import app
from ....serializers import BooleanField, Err, Ok, make_response


@app.get("/ingredient_attributes/<name>")
@make_response
def get_ingredient_attribute(name: str):
    print(name, flush=True)
    with IngredientManager() as manager:
        try:
            attribute = manager.get_attribute(name=name)
        except NotFound:
            return Err(f"Attribute with name {name} not found")
    return Ok(attribute)
