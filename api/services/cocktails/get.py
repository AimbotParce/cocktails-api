import flask

from database.managers import CocktailManager

from ... import app
from ...serializers import BooleanField, Err, Ok, make_response


@app.get("/cocktails")
@make_response
def get_cocktails():
    limit = flask.request.args.get("limit", None, type=int)
    offset = flask.request.args.get("offset", 0, type=int)
    alcoholic = flask.request.args.get("alcoholic", False, type=BooleanField)

    with CocktailManager() as manager:
        uuid = manager.get_cocktails(limit=limit, offset=offset, alcoholic=alcoholic)
    return Ok(uuid)
