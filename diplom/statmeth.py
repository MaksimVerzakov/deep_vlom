from pymongo import Connection

class ThemeDict(object):

    def __init__(self, name, dict=None):
        self.dict = dict
        self.name = name

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
