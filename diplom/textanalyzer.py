from cement2.core import backend, foundation, controller, handler
from base import crete_base
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
        netpath = self.pargs.netpath or None
        if not netpath:
            crete_base(path, host, port, name)

    @controller.expose(help="another base controller command")
    def create_base(self):
        path = self.pargs.basepath
        host = self.pargs.host or MONGODB_BACKEND_SETTINGS['host']
        port = self.pargs.port or MONGODB_BACKEND_SETTINGS['port']
        name = self.pargs.name or MONGODB_BACKEND_SETTINGS['database']
        crete_base(path, host, port, name)


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
