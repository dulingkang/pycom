from tornado.web import RequestHandler
from handler import route
from model.commodity import Commodity


@route('/commodity/(\d+)/info')
class getCommodityInfoHandler(RequestHandler):

    async def get(self, id):
        com = Commodity.get(id)
        if not com:
            raise
        self.write({'info': {'price': round(float(com.price), 2), 'title': com.title}})
