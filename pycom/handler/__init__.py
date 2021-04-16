from tornado.web import url, StaticFileHandler

route_modules = [
    'pycom.handler.commodity'
]


class route(object):
    _routes = []

    def __init__(self, uri, name=None):
        self._uri = uri
        self.name = name

    def __call__(self, _handler):
        uri = self._uri
        if hasattr(_handler, 'url_prefix'):
            uri = "%s%s" % (_handler.url_prefix, uri)
        name = self.name or _handler.__name__
        self._routes.append(url(uri, _handler, name=name))
        return _handler

    @classmethod
    def get_routes(cls):
        for r in route_modules:
            __import__(r)
        static_handler = url(r'/static/(.*)', StaticFileHandler)
        if static_handler not in cls._routes:
            cls._routes.append(static_handler)
        return cls._routes