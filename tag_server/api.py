import json

from flask import request

from models import Remarketing, OpenCarts, OriginPurchases

page_size = 100


def get_pagination_offset():
    query_args = request.args.to_dict()
    page = query_args.get('page', 0)
    return page_size * page


def get_paged_data(model):
    offset = get_pagination_offset()
    items = [i.to_dict() for i in model.objects.skip(offset).limit(page_size).all()]
    return items


def get_api():
    class APIFactory(object):
        @staticmethod
        def get_remarketing():
            """
            Get remarketing information collected by tags
            :return:
            """
            data = get_paged_data(Remarketing)
            return json.dumps(data)

        @staticmethod
        def get_open_carts():
            """
            Get open carts collected by tags
            :return:
            """
            data = get_paged_data(OpenCarts)
            return json.dumps(data)

        @staticmethod
        def get_purchases():
            """
            Get purchases
            :return:
            """
            data = get_paged_data(OriginPurchases)
            return json.dumps(data)

    return APIFactory
