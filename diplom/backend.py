from pymongo import Connection

class TextBase(object):
    vocabulary = []
    
    def __init__(self, host, port, db_name):
        connection = Connection(host=host, port=port)
        db = connection[db_name]
        self.collection = db['text_collection']
    
    def append(self, class_name, words_dict):
        for word in words_dict:
            if word not in vocabulary:
                vocabulary.append(word)
        word_dict['_class_name'] = class_name
        self.collection.insert(word_dict)
    
    def _normalize(self):
        doc_count = self.collection.count()
        for word in self.vocabulary:
            docs = self.collection.find({word : {"$exists" : True}})
            for doc in docs:
                tf = doc[word]
                idf = math.log(doc_count/docs.count())
                self.collection.update(doc, {'$set' : {word : tf*idf}})

