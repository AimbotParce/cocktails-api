import io

import psycopg2

from ..models import Image, Ingredient, IngredientAttribute
from . import Manager


class AttachmentManager(Manager):
    def add_image(self, name: str, image: io.BytesIO) -> str:
        "Create an image and return its uuid"
        image = Image(name=name, image=psycopg2.Binary(image.read()))
        self.session.add(image)
        self.session.commit()
        return image.uuid

    def get_image(self, uuid: str) -> io.BytesIO:
        "Get an image by its uuid"
        image = self.session.query(Image).filter_by(uuid=uuid).first()
        return io.BytesIO(image.image)
