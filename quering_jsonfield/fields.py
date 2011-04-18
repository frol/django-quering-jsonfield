class JSONField(models.TextField):
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        if value:
            value = json.loads(value)
        else:
            value = {}
        return value

    def get_db_prep_save(self, value):
        value = json.dumps(value)
        return super(JSONField, self).get_db_prep_save(value)
