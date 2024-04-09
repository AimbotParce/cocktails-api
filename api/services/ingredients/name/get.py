import flask
from database.exceptions import NotFound
from database.managers import IngredientManager

from .... import app
from ....serializers import BooleanField, Err, Ok, make_response


@app.get("/ingredients/<name>")
@make_response
def get_ingredient(name: str):
    with IngredientManager() as manager:
        try:
            ingredient = manager.get_ingredient(name=name)
        except NotFound:
            return Err(f"Ingredient with name {name} not found")
    return Ok(ingredient)
