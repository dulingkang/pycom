import os
import tornado.options
import tornado.httpserver
from handler import route
from tornado.options import options, define


define('port', default="8333", help='run on the given port', type=int)

if __name__ == '__main__':
    root_dir = os.path.dirname(os.path.abspath(__file__))
    settings = dict(
        autoreload=True,
        websocket_ping_intervel=10
    )
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=route.get_routes(), **settings)
    httpserver = tornado.httpserver.HTTPServer(app, xheaders=True)
    address = '127.0.0.1'
    httpserver.listen(port=options.port, address=address)
    loop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(loop)
    loop.start()
