from core.store import store
from model import BaseModel


class Commodity(BaseModel):

    table = 'commodity'
    fields = [
        'id',
        'item_id',
        'title',
        'price',
        'cover',
        'desc',
        'create_time',
        'update_time',
    ]

    @classmethod
    def get_id_by_item_id(cls, item_id):
        rs = store.execute("select id from {} where item_id=%s".format(cls.table), item_id)
        return rs[0][0] if rs else 0

    @classmethod
    def get_by_item_id(cls, item_id):
        _id = cls.get_id_by_item_id(item_id)
        return cls.get(_id)
