import flask

from database.managers import CocktailManager

from ... import app
from ...serializers import BooleanField, Err, Ok, make_response


@app.get("/cocktails")
@make_response
def get_all_cocktails():
    limit = flask.request.args.get("limit", None, type=int)
    offset = flask.request.args.get("offset", 0, type=int)

    with CocktailManager() as manager:
        cocktails = manager.get_cocktails(limit=limit, offset=offset)
    return Ok(cocktails)
