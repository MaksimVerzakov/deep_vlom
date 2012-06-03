from pymongo import Connection

class ThemeDict(object):

    def __init__(self, host, port, db_name):
        connection = Connection(host=host, port=port)
        db = connection[db_name]
        self.collection = db['stat_collection']

    def classify(self, words_dict):
        best = {'theme': None, 'weight': 0.0}
        near = {'theme': None, 'weight': 0.0}
        for theme in self.collection.find():
            weight = 0.0
            for word in theme['stat']:
                words_weight = theme['stat'][word]
                weight += words_dict.get(word, 0.0) * words_weight
            if weight > best['weight']:
                near['theme'] = best['theme']
                near['weight'] = best['weight']
                best['theme'] = theme['_cls']
                best['weight'] = weight
        return best, near
