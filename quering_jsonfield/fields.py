import json

from django.db import models

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^quering_jsonfield\.fields\.JSONField"])
except:
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

    def get_db_prep_save(self, value, *args, **kwargs):
        value = json.dumps(value)
        return super(JSONField, self).get_db_prep_save(value, *args, **kwargs)
