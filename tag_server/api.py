import json

from flask import request

from models import Remarketing, OpenCarts, OriginPurchases

import pymongo

page_size = 100


def get_pagination_offset():
    query_args = request.args.to_dict()
    page = int(query_args.get('page', 0))
    return page_size * page


def get_paged_data(model):
    offset = get_pagination_offset()
    order = get_ordering(model)
    items = [i.to_dict() for i in model.objects.order_by(*order).skip(offset).limit(page_size).all()]
    return items


def get_ordering(model):
    query_args = request.args.to_dict()
    order_str = query_args.get('order', '')
    order_bits = [o.strip() for o in order_str.split(',') if len(o.strip()) > 0]
    order = []

    if len(order_bits) < 1:
        return ['id']

    for bit in order_bits:
        bit_name = bit[1:] if bit[0] in ['+', '-'] else bit
        bit_sorting = '-' if bit[0] == '-' else ''

        if bit_name in dir(model):
            order.append(bit_sorting + bit_name)

    return order


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
