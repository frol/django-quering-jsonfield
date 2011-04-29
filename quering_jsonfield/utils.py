from django.utils import simplejson


class JSONDict(dict):
    
    def __repr__(self):
        return unicode(simplejson.dumps(self, indent=4))
