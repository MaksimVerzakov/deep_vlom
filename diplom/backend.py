import math
from copy import copy
from bson.code import Code
from pymongo import Connection

class TextBase(object):
    vocabulary = set()
    weight_corrector = {}
    classes = []

    def __init__(self, host, port, db_name):
        connection = Connection(host=host, port=port)
        db = connection[db_name]
        self.collection = db['text_collection3']
        self.stat = db['stat_collection1']
        self.count = self.collection.count()
        #self._normalize()

    def append(self, class_name, words_dict):
        words_dict['_class_name'] = class_name
        self.collection.insert(words_dict)
        self.count += 1

    def _normalize(self):
        print 'Normalize'
        for doc in self.collection.find():
            if doc['_class_name'] not in self.classes:
                self.classes.append(doc['_class_name'])
        doc_count = self.collection.count()
        for doc in self.collection.find():
            self.vocabulary = self.vocabulary | set(doc.keys())
        if self.vocabulary:
            self.vocabulary.remove('_id')
            self.vocabulary.remove('_class_name')
        print len(self.vocabulary)
        #for word in self.vocabulary:
        #    docs = self.collection.find({word: {"$exists": True}}).count()
        #    self.weight_corrector[word] = math.log(doc_count/docs)
        print 'Normalized'

    def corect_weight(self, doc):
        '''Return list of TF-IDF weights for doc'''
        res = []
        for word in self.weight_corrector:
            res.append(self.weight_corrector[word] * doc.get(word, 0.0))
        return res

    def to_stat(self):
        for cls in self.classes:
            print cls
            docs = self.collection.find({'_class_name' : cls})
            cls_dict = {}
            for doc in docs:
                print 'weight corrector'
                for word in self.weight_corrector:
                    correct = self.weight_corrector[word] * doc.get(word, 0.0) #tf_idf
                    correct /= float(docs.count()) #average
                    if word not in cls_dict:
                        cls_dict[word] = 0.0
                    cls_dict[word] += correct
                    if cls_dict[word] == 0.0:
                        cls_dict.pop(word)
            print len(cls_dict)
            self.stat.insert({'_cls': cls,
                              'stat': cls_dict})
        print 'to stat endeded'

    def to_lists(self):
        input = []
        target = []
        print 'start to list'
        for cls in self.classes:
            docs = self.collection.find({'_class_name' : cls})
            for doc in docs:
                input.append(self.to_list(doc))
            target.extend([self.classes.index(cls) for x in range(docs.count())])
        print 'end to list'
        return input, target

    def to_list(self, doc):
        return [doc.get(x, 0.0) for x in self.vocabulary]
