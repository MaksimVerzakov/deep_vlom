import os
from cement2.core import backend, foundation, controller, handler
from base import create_base
from backend import TextBase
from statmeth import *
from settings import TEXT_DIR, MONGODB_BACKEND_SETTINGS


class MyAppBaseController(controller.CementBaseController):
    class Meta:
        label = 'base'
        description = "Text Analyzer"

        arguments = [
            (['-t', '--textpath'], dict(action='store', help='path to file to check')),
            (['-b', '--basepath'], dict(action='store', help='path to base')),
            (['-d', '--dumppath'], dict(action='store', help='path to dump')),
            (['-n', '--netpath'], dict(action='store', help='path to neural net')),
            (['-s', '--smooth'], dict(action='store', help='smooth')),
            (['--host'], dict(action='store', help='Host of DB')),
            (['--port'], dict(action='store', help='Port of DB')),
            (['--name'], dict(action='store', help='Name of DB')),
            (['-C'], dict(action='store_true', help='the big C option'))
            ]

    @controller.expose(hide=True, aliases=['run'])
    def default(self):
        path = self.pargs.textpath or TEXT_DIR
        host = self.pargs.host or MONGODB_BACKEND_SETTINGS['host']
        port = self.pargs.port or MONGODB_BACKEND_SETTINGS['port']
        name = self.pargs.name or MONGODB_BACKEND_SETTINGS['database']
        #netpath = self.pargs.netpath or None
        #if not netpath:
        #    crete_base(path, host, port, name)

    @controller.expose(help="another base controller command")
    def create_base(self):
        path = self.pargs.basepath
        host = self.pargs.host or MONGODB_BACKEND_SETTINGS['host']
        port = self.pargs.port or MONGODB_BACKEND_SETTINGS['port']
        name = self.pargs.name or MONGODB_BACKEND_SETTINGS['database']
        #import pdb; pdb.set_trace()
        b = create_base(path, host, port, name)
        b.to_stat()

    @controller.expose(help="another base controller command")
    def check_svm(self):
        host = self.pargs.host or MONGODB_BACKEND_SETTINGS['host']
        port = self.pargs.port or MONGODB_BACKEND_SETTINGS['port']
        name = self.pargs.name or MONGODB_BACKEND_SETTINGS['database']
        from mysvm import SVM
        base = TextBase(host, port, name)
        input, target = base.to_lists()
        s = SVM(input, target)
        #testing
        from pymongo import Connection
        connection = Connection(host=host, port=port)
        db = connection[name]
        collection = db['test_collection2']
        docs = collection.find()
        count = 0.0
        for doc in docs:
            res = s.predict(base.to_list(doc))
            if doc['_class_name'] == base.classes[int(res)]:
                count += 1
        print count / docs.count() * 100

    @controller.expose(help="another base controller command")
    def study_bigram(self):
        base = {}
        path = self.pargs.basepath
        d_path = self.pargs.dumppath
        for theme in os.listdir(path):
            docs_dir = os.path.join(path, theme)
            for doc in os.listdir(docs_dir):
                if theme not in base:
                    base[theme] = []
                f = open(os.path.join(docs_dir, doc))
                base[theme].append(f.readlines())
        from LaplaceBigramLanguageModel import LaplaceBigramLanguageModel
        for theme in base:
            print theme
            dump_path = os.path.join(d_path, theme)
            LaplaceBigramLanguageModel(base[theme]).dumps(dump_path)
        print 'ok'

    @controller.expose(help="another base controller command")
    def check_bigram(self):
        path = self.pargs.basepath
        text = self.pargs.textpath
        smooth = float(self.pargs.smooth)
        from LaplaceBigramLanguageModel import LaplaceBigramLanguageModel
        prob = {}
        for theme in os.listdir(path):
            docs_dir = os.path.join(path, theme)
            prob[theme] = LaplaceBigramLanguageModel()
            prob[theme].loads(docs_dir)
        print 'testing...'
        exact_res = 0.0
        approx_res = 0.0
        count = 0
        now = 0
        for theme in os.listdir(text):
            print theme
            docs_dir = os.path.join(text, theme)
            for doc in os.listdir(docs_dir):
                now += 1
                f = open(os.path.join(docs_dir, doc))
                txt = f.readlines()
                scores = {}
                for p in prob:
                    scores[p] = prob[p].score(txt, smooth)
                res = scores.items()
                res.sort(key=lambda x: x[1])
                if theme == res[-1][0]:
                    exact_res += 1
                if theme in [x[0] for x in res[-2:]]:
                    approx_res += 1.0
                count += 1
                print 'Exact_result: %s %%' % (exact_res / count * 100)
                print 'Approx_result: %s %%' % (approx_res / count * 100)

    @controller.expose(help="another base controller command")
    def check_static(self):
        host = self.pargs.host or MONGODB_BACKEND_SETTINGS['host']
        port = self.pargs.port or MONGODB_BACKEND_SETTINGS['port']
        name = self.pargs.name or MONGODB_BACKEND_SETTINGS['database']
        from pymongo import Connection
        #base = TextBase(host, port, name)
        td = ThemeDict(host, port, name)
        connection = Connection(host=host, port=port)
        db = connection[name]
        collection = db['test_collection2']
        exact_res = 0.0
        approx_res = 0.0
        docs = collection.find()
        for doc in docs:
            res, near = td.classify(doc)
            diff = res['weight'] - near['weight']
            print 'actual: %s, got: %s, near: %s, diff: %s' % (doc['_class_name'],
                                                     res['theme'],
                                                     near['theme'],
                                                     diff)
            if '004' == res['theme']:
                exact_res +=1
                approx_res += 1

            if '004' == near['theme'] and diff < 0.1**-5:
                approx_res +=1
        exact_res /= float(docs.count()) / 100
        print '%s %%' % exact_res
        approx_res /= float(docs.count()) / 100
        print '%s %%' % approx_res
        print 'ok'


class MyApp(foundation.CementApp):
    class Meta:
        label = 'textanalyzer'
        base_controller = MyAppBaseController


if __name__=='__main__':
    app = MyApp()
    app.setup()
    try:
        app.run()
    finally:
        app.close()
