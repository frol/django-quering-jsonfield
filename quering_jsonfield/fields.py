from django.db import models
from django.utils import simplejson as json

from .utils import JSONDict


class JSONField(models.TextField):
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if value:
            value = JSONDict(json.loads(value))
        else:
            value = JSONDict()
        return value

    def get_db_prep_save(self, value):
        value = json.dumps(value)
        return super(JSONField, self).get_db_prep_save(value)
