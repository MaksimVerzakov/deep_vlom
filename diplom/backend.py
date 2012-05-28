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
        self.collection = db['text_collection2']
        self.count = self.collection.count()
        self._normalize()

    def append(self, class_name, words_dict):
        words_dict['_class_name'] = class_name
        self.collection.insert(words_dict)
        self.count += 1

    def _normalize(self):
        print 'Normalize'
        doc_count = self.collection.count()
        for doc in self.collection.find():
            self.vocabulary = self.vocabulary | set(doc.keys())
        self.vocabulary.remove('_id')
        self.vocabulary.remove('_class_name')
        print len(self.vocabulary)
        for word in self.vocabulary:
            docs = self.collection.find({word: {"$exists": True}}).count()
            self.weight_corrector[word] = math.log(doc_count/docs)
        print 'Normalized'

    def corect_weight(self, doc):
        res = []
        for word in self.weight_corrector:
            res.append(self.weight_corrector[word] * doc.get(word, 0.0))
        return res

    def to_dict(self):
        classes = []
        d = {}
        print 'to dict started'
        for doc in self.collection.find():
            if doc['_class_name'] not in classes:
                classes.append(doc['_class_name'])
        for cls in classes:
            d[cls] = []
            for doc in self.collection.find({'_class_name' : cls}):
                d[cls].append(self.corect_weight(doc))
        print 'to dict endeded'
        return d

    def to_lists(self):
        d = self.to_dict()
        input = []
        target = []
        print 'start to list'
        for el in d:
            input.extend(d[el])
            null_tar = [0.0 for x in range(len(d))]
            null_tar[d.keys().index(el)] = 1.0
            target.extend([null_tar for x in range(len(d[el]))])
        print 'end to list'
        return input, target

class In_Out(object):
    def __init__(self, host, port, db_name):
        connection = Connection(host=host, port=port)
        db = connection[db_name]
        self.collection = db['in_out']

    def append(self, name, input, target, weight_corrector):
        self.collection.insert({'name': name,
                                'input': input,
                                'target': target,
                                'weight_corrector': weight_corrector})

    def get(name):
        return self.collection.findone({'name': name})



