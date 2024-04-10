import flask
from database.exceptions import NotFound
from database.managers import AttachmentManager

from ..... import app
from .....serializers import BooleanField, Err, Ok, make_response


@app.delete("/attachments/images/<uuid>")
@make_response
def delete_image(uuid: str):
    with AttachmentManager() as manager:
        try:
            manager.delete_image(uuid=uuid)
        except NotFound:
            return Err(f"Image with UUID {uuid} not found")

    return Ok()
