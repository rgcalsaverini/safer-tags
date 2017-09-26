import json
from time import time

from flask import session, request
from redis.lock import Lock as RedisLock

from tag_server import gen_error

valid_pagetypes = ['product']


def generic_data(store_id, tag_type):
    """
    Assemble a generic data payload for the tag. Could be supplemented by specific tags.

    :param store_id: And arbitrary ID identifying the store
    :param tag_type: The type of the tag being collected. Ex: pageview
    :return: The data object
    """
    data = get_request_data()

    return {
        'tag_type': tag_type,
        'user_id': session['user_id'] if 'user_id' in session else '(not set)',
        'origin': data.get('origin', 'direct'),
        'received_at': int(time()),
        'store_id': store_id,
        'products': data.get('products', [])
    }


def enqueue_tag(payload, redis_connection, enqueue_lock):
    """
    Enqueue the tag to be processed later, as to not delay user response.
    Obviously, this locking solution is a major bottleneck, and a hindrance to
    scalability. It servers the example, but should be replaced by a more robust
    solution on a real server.

    :param payload: The data payload for the tag
    :param redis_connection:
    :param enqueue_lock:
    :return:
    """
    enqueue_lock.acquire()
    last_idx = int(redis_connection.get('last_queue_idx'))
    redis_connection.incr('last_queue_idx')
    enqueue_lock.release()

    redis_connection.rpush('tag_queue', last_idx)
    redis_connection.set('tag_data[{}]'.format(last_idx), json.dumps(payload))


def get_request_data():
    """
    Get all the data passed to the request on a single dictionary
    :return: A dictionary of all the data
    """
    query_args = request.args.to_dict()
    form_args = request.form.to_dict()
    try:
        json_args = request.get_json(force=True)
    except TypeError:
        json_args = dict()

    all_data = {**query_args, **form_args, **json_args}

    results = dict()

    for k, v in all_data.items():
        try:
            val = json.loads(v) if type(v) is str else v
        except ValueError:
            val = str(v)

        results[k] = val

    return results


def get_collectors(redis_ref, app_ref):
    """
    Forms the collector factory.

    :param redis_ref: A redis connection object
    :param app_ref: A flask application object
    :return:
    """
    redis = redis_ref
    app = app_ref
    enqueue_lock = RedisLock(redis_ref, 'enqueue_lock')

    class CollectorsFactory(object):
        @staticmethod
        def pageview(store_id, pagetype):
            """
            Collects a simple pageview tag

            :param store_id: And arbitrary ID identifying the store
            :param pagetype: One of the valid pagetipes on 'valid_pagetypes'
            :return: An empty HTTP response (204, no content)
            """
            if pagetype not in valid_pagetypes:
                return gen_error('invalid_pagetype', pagetype)

            pageview_data = generic_data(store_id, 'pageview')
            pageview_data['pagetype'] = pagetype

            enqueue_tag(pageview_data, redis, enqueue_lock)

            return '', 204

        @staticmethod
        def add_to_cart(store_id):
            """
            Collects a 'add to cart' event tag

            :param store_id: And arbitrary ID identifying the store
            :return: An empty HTTP response (204, no content)
            """

            event_data = generic_data(store_id, 'add_to_cart')
            enqueue_tag(event_data, redis, enqueue_lock)

            return '', 204

        @staticmethod
        def purchase(store_id, total, tr_id):
            """
            Collects a 'purchase' event tag

            :param store_id: And arbitrary ID identifying the store
            :param total: The transaction's total value
            :param transaction_id: The transaction's id
            :return: An empty HTTP response (204, no content)
            """

            event_data = generic_data(store_id, 'purchase')
            event_data['total'] = float(total) / 100
            event_data['transaction_id'] = tr_id
            enqueue_tag(event_data, redis, enqueue_lock)

            return '', 204

    return CollectorsFactory


"https://www.fastshop.com.br/loja/liquidificador-oster-classico-03-velocidades-prata-004655-fast"
