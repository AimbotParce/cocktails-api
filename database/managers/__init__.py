from ..databases import database


class Manager:
    DATABASE = database

    def __init__(self):
        self.session = self.DATABASE.session()

    def end(self):
        self.session.commit()
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.end()

    def __del__(self):
        self.end()


from .attachments import AttachmentManager
from .cocktails import CocktailManager

__all__ = ["Manager", "CocktailManager", "AttachmentManager"]
