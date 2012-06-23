from django.db import models
from django.utils import simplejson as json

try:
    from south.modelsinspector import add_ignored_fields
    add_ignored_fields(["^quering_jsonfield\.fields\.JSONField"])
except ImportError:
    pass

from .utils import JSONDict


class JSONField(models.TextField):
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if value:
            if isinstance(value, dict):
                value = JSONDict(value)
            elif isinstance(value, (unicode, str)):
                value = JSONDict(json.loads(value))
        else:
            value = JSONDict()
        return value

    def get_db_prep_save(self, value):
        value = json.dumps(value)
        return super(JSONField, self).get_db_prep_save(value)
