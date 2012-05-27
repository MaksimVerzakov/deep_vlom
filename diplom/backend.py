from math import log
from copy import copy

from pymongo import Connection
from bson.code import Code

class TextBase(object):
    vocabulary = set()

    def __init__(self, host, port, db_name):
        connection = Connection(host=host, port=port)
        db = connection[db_name]
        self.collection = db['text_collection']

    def append(self, class_name, words_dict):
        words_dict['_class_name'] = class_name
        self.collection.insert(words_dict)

    def _normalize(self):
        doc_count = self.collection.count()
        for doc in self.collection.find():
            self.vocabulary = self.vocabulary | set(doc.keys())
        print len(self.vocabulary)
        for word in copy(self.vocabulary):
            docs = self.collection.find({word : {"$exists" : True}})
            if float(docs.count())/float(doc_count) > 0.85:
                self.vocabulary.remove(word)
        print len(self.vocabulary)
            #for doc in docs:
            #    tf = doc[word]
            #    idf = log(doc_count/doc_count)
            #    self.collection.update(doc, {'$set' : {word : tf*idf}})

    def to_dict(self):
        map = Code()
        d = {}
        for doc in self.collection.find():
            if not d.get(doc['_class_name'], None):
                d[doc['_class_name']] = []
            tmp_list = []
            for i in self.vocabulary:
                tmp_list.append(el.get(i, 0.0))
            d[doc['_class_name']].append(tmp_list)
        return d

