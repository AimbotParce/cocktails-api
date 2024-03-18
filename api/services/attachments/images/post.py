import flask

from database.managers import AttachmentManager

from .... import app
from ....serializers import Err, Ok, make_response


@app.post("/attachments/images")
@make_response
def post_image():
    if not "file" in flask.request.files:
        return Err("Missing file")
    file = flask.request.files["file"]

    with AttachmentManager() as manager:
        image = manager.add_image(name=file.filename, image=file.stream)
    return Ok(image)
