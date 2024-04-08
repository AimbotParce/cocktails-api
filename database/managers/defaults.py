import io

from ..exceptions import NotFound
from ..models import DefaultValue
from ..models.defaults import DefaultValueJSON
from . import Manager


class DefaultsManager(Manager):
    def set(self, key: str, value: str) -> DefaultValueJSON:
        default = self.session.query(DefaultValue).filter_by(key=key).first()
        if not default:
            default = DefaultValue(key=key, value=value)
            self.session.add(default)
        else:
            default.value = value
        return default.to_json()

    def get(self, key: str) -> str:
        value = self.session.query(DefaultValue).filter_by(key=key).first()
        if not value:
            raise NotFound()
        return value.value

    def __contains__(self, key: str) -> bool:
        return self.session.query(DefaultValue).filter_by(key=key).count() > 0
