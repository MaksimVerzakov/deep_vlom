import math
from copy import copy
from bson.code import Code
from pymongo import Connection

class TextBase(object):
    vocabulary = set()
    weight_corrector = {}
    count = 0

    def __init__(self, host, port, db_name):
        connection = Connection(host=host, port=port)
        db = connection[db_name]
        self.collection = db['text_collection']
        self.count = self.collection.count()
        self._normalize()

    def append(self, class_name, words_dict):
        words_dict['_class_name'] = class_name
        self.collection.insert(words_dict)
        self.count += 1

    def _normalize(self):
        doc_count = self.collection.count()
        for doc in self.collection.find():
            self.vocabulary = self.vocabulary | set(doc.keys())
        print len(self.vocabulary)
        import pdb; pdb.set_trace()
        for word in self.vocabulary:
            docs = self.collection.find({'words.keys()' : word})
            self.weight_corrector[word] = math.log(doc_count/doc_count)

    def corect_weight(self, doc):
        res = {}
        for word in weight_corrector:
            res[word] = self.weight_corrector[word] * doc.get(word, 0)
        return res

    def to_dict(self):
        map = Code("function () {"
                   "  emit(this._class_name, this.words);"
                   "}")
        reduce = Code("function (key, values) {"
                      "  var res = [];"
                      "  for(d in values){"
                      "      res[res.length] = values;"
                      "   }"
                      "  return res;"
                      "}")
        classes = []
        for doc in self.collection.find():
            if doc['_class_name'] not in classes:
                classes.append(doc['_class_name'])
        d = {}
        for cls in classes:
            d[cls] = []
            for doc in self.collection.find({'_class_name' : cls}):
                d[cls].append(doc)
        return d


