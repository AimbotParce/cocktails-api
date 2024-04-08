import flask
from database.managers import AttachmentManager

from .... import app
from ....serializers import BooleanField, Err, Ok, make_response


@app.get("/attachments/images")
@make_response
def get_all_images():
    limit = flask.request.args.get("limit", None, type=int)
    offset = flask.request.args.get("offset", 0, type=int)

    with AttachmentManager() as manager:
        images = manager.get_images(limit=limit, offset=offset)
    return Ok(images)
