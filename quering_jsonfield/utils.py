import json

class JSONDict(dict):
    
    def __repr__(self):
        return unicode(json.dumps(self, indent=4))
