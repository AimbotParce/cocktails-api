import flask

from database.exceptions import NotFound
from database.managers import AttachmentManager

from ..... import app
from .....serializers import BooleanField, Err, Ok, make_response


@app.get("/attachments/images/<uuid>")
def get_image(uuid: str):
    with AttachmentManager() as manager:
        try:
            image = manager.get_image(uuid=uuid)
        except NotFound:
            return Err(f"Image with UUID {uuid} not found")

    return flask.send_file(image, mimetype="image/jpeg")
