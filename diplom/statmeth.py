from pymongo import Connection

class ThemeDict(object):

<<<<<<< HEAD
    def __init__(self, host, port, db_name):
        connection = Connection(host=host, port=port)
        db = connection[db_name]
        self.collection = db['stat_collection']
=======
    def __init__(self, name, dict=None):
        self.dict = dict
        self.name = name
>>>>>>> 002910871571d75fa29c8f909e8e569d645818f9

    def score(self, words_dict):
        weight = 0.0
        for word in theme['stat']:
            words_weight = theme['stat'][word]
            weight += words_dict.get(word, 0.0) * words_weight
        return weight

    def dumps(self, path):
        f = open(path, 'wb+')
        f.write(json.dumps(self.dict))

    def loads(self, path):
        f = open(path, 'r+')
        self.unigramCounts = json.loads(f.readline())
