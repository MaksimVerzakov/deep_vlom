class ThemeDict(object):
    theme_dict = {}

    def __init__(self, collection):
        for el in collection.find():
            name = el['_class_name']
            if name not in theme_dict:
                self.theme_dict[name] = {}
            for word in el:
                if not word.startswith('_'):
                    self.theme_dict[name][word] = self.theme_dict[name].get(word, 0.0) + el[word]

    def classify(self, words_dict):
        best = {'theme': None, 'weight': 0.0}
        for theme in self.theme_dict:
            weight = 0.0
            for word in words_dict:
                weight += words_dict[word]*self.theme_dict[theme].get(word, 0.0)
            if weight > best['weight']:
                best['theme'] = theme
                best['weight'] = weight
        return best
