import io

import psycopg2

from ..exceptions import NotFound
from ..models import Image, Ingredient, IngredientAttribute
from ..models.images import ImageJSON
from . import Manager


class AttachmentManager(Manager):
    def add_image(self, name: str, image: io.BytesIO) -> ImageJSON:
        "Create an image and return its uuid"
        image = Image(name=name, image=image.read())
        self.session.add(image)
        self.session.commit()
        return image.to_json()

    def get_image(self, uuid: str) -> io.BytesIO:
        "Get an image by its uuid"
        image = self.session.query(Image).filter_by(uuid=uuid).first()
        if not image:
            raise NotFound()
        return io.BytesIO(image.image)
