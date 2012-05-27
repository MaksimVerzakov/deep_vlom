from cement2.core import backend, foundation, controller, handler
from base import crete_base
from neuralnet import NeuralNet
from backend import TextBase
from settings import TEXT_DIR, MONGODB_BACKEND_SETTINGS

class MyAppBaseController(controller.CementBaseController):
    class Meta:
        label = 'base'
        description = "Text Analyzer"

        #config_defaults = dict(
        #    path=TEXT_DIR,
        #   )

        arguments = [
            (['-t', '--textpath'], dict(action='store', help='path to file to check')),
            (['-b', '--basepath'], dict(action='store', help='path to base')),
            (['-n', '--netpath'], dict(action='store', help='path to neural net')),
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
<<<<<<< HEAD
        from backend import TextBase
        tb = TextBase(host, port, name)
        tb._normalize()
=======
        base = TextBase(host, port, name)
        base.to_dict()
>>>>>>> f5f0467622156d24492931ddd1d81e4284022149
        #netpath = self.pargs.netpath or None
        #if not netpath:
        #    crete_base(path, host, port, name)

    @controller.expose(help="another base controller command")
    def create_base(self):
        path = self.pargs.basepath
        host = self.pargs.host or MONGODB_BACKEND_SETTINGS['host']
        port = self.pargs.port or MONGODB_BACKEND_SETTINGS['port']
        name = self.pargs.name or MONGODB_BACKEND_SETTINGS['database']
        crete_base(path, host, port, name)

    @controller.expose(help="another base controller command")
    def create_net(self):
        path = self.pargs.basepath
        host = self.pargs.host or MONGODB_BACKEND_SETTINGS['host']
        port = self.pargs.port or MONGODB_BACKEND_SETTINGS['port']
        name = self.pargs.name or MONGODB_BACKEND_SETTINGS['database']
        from backend import TextBase
        base = TextBase(host, port, name)
        import pdb; pdb.set_trace()
        t0 = len(base.vocabulary)
        t1 = int(len(base.vocabulary)*1.5)
        net = NeuralNet([t0, t1, base.count])
        net.train(base.to_dict())

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
