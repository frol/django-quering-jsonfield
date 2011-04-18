import itertools

from django.db import models


class JSONAwareQuerySet(models.query.QuerySet):
    def __init__(self, json_fields = [], *args, **kwargs):
        self.json_fields = json_fields
        super(JSONAwareQuerySet, self).__init__(*args, **kwargs)
        
    def _filter_or_exclude(self, negate, *args, **kwargs):
        extra_lookups = {}
        
        for lookup in kwargs:
            if lookup.split('__')[0] in self.json_fields:
                extra_lookups[lookup] = kwargs[lookup]

        [kwargs.pop(key) for key in extra_lookups]

        clone = super(JSONAwareQuerySet, self)._filter_or_exclude(negate, *args, **kwargs)
        
        result = []
        
        if extra_lookups.keys():
            len(clone) # Fill the cache
            
            for item, lookup in itertools.product(self, extra_lookups.keys()):
                if not negate and self._evaluate_json_lookup(item, lookup, extra_lookups[lookup]):
                    result.append(item)
                elif negate and not self._evaluate_json_lookup(item, lookup, extra_lookups[lookup]):
                    result.append(item)

            clone._result_cache = result

        return clone
        
    def _evaluate_json_lookup(self, item, lookup, value):
        oper = 'exact'
        
        evaluators = {
            'icontains': lambda item, value: item.lower() in value.lower(),
            'contains': lambda item, value: item in value,
            'in': lambda item, value: item in value,
            'iexact': lambda item, value: item.lower() == value.lower(),
            'exact': lambda item, value: item == value,
            'lt': lambda item, value: item < value,
            'lte': lambda item, value: item <= value,
            'gt': lambda item, value: item > value,
            'gte': lambda item, value: item >= value,
        }
        
        def _getattr(obj, key):
            if isinstance(obj, dict):
                return obj[key]
            return getattr(obj, key)

        if lookup.split('__')[-1] in evaluators.keys():
            oper = lookup.split('__')[-1]
            lookup = '__'.join(lookup.split('__')[:-1])

        field = item

        for key in lookup.split('__'):
            try:
                field = _getattr(field, key)
            except (AttributeError, KeyError):
                return False

        return evaluators[oper](field, value)
        
    def count(self):
        return super(JSONAwareQuerySet, self).count()


class JSONAwareManager(models.Manager):
    def __init__(self, json_fields = [], *args, **kwargs):
        self.json_fields = json_fields
        super(JSONAwareManager, self).__init__(*args, **kwargs)
        
    def get_query_set(self):
        return JSONAwareQuerySet(self.json_fields, self.model)
