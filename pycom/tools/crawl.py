import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
from pycom.model.commodity import Commodity



SQKB_URL = 'https://www.sqkb.com/g/getCouponTopicList'


def crawl(page=1, cid=2):
    params = {
        'sort': 0,
        'cid': cid,
        'page': page,
        'pagesize': 40,
    }
    res = {}
    try:
        res = requests.get(SQKB_URL, params=params)
        res = res.json()
        convert_data(res)
    except Exception as e:
        print(e)
    return res


def convert_data(d):
    coupon_lists = d['data']['coupon_list']
    for coupon_list in coupon_lists:
        title = coupon_list['title']
        price = coupon_list['zk_price']
        item_id = coupon_list['item_id']
        cover = coupon_list['pic']
        save_crawl_item(item_id, title, price, cover)


def save_crawl_item(item_id, title, price, cover):
    com = Commodity.get_by_item_id(item_id)
    if not com:
        Commodity.add(item_id=item_id, title=title, price=price, cover=cover)
    else:
        Commodity.update(com.id, title=title, price=price, cover=cover)


if __name__ == '__main__':
     crawl()
