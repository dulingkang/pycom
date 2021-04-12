from tornado.web import RequestHandler
from handler import route



@route('/commodity/info')
class getCommodityInfoHandler(RequestHandler):

    async def get(self):
        self.write({'info': {'price': 10, 'title': 'test'}})
