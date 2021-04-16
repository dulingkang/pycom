from tornado.web import RequestHandler
from pycom.handler import route
from pycom.model.commodity import Commodity


@route('/commodity/(\d+)/info')
class GetCommodityInfoHandler(RequestHandler):

    async def get(self, id):
        com = Commodity.get(id)
        if not com:
            raise
        self.write({'info': {'price': round(float(com.price), 2), 'title': com.title}})


@route('/check')
class CheckHandler(RequestHandler):
    async def get(self):
        self.write({'status': 'ok'})
