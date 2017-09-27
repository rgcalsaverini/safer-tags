import json
from time import time

from models import Remarketing, OpenCarts, OriginPurchases
from tag_server import initiate_mongo_connection, create_redis_connection

initiate_mongo_connection()
redis = create_redis_connection()


def tag_data_key(idx):
    return 'tag_data[{}]'.format(int(idx.decode('utf-8')))


def get_next_tag():
    tag_id = redis.lpop('tag_queue')

    if not tag_id:
        return

    data_key = tag_data_key(tag_id)

    if not redis.exists(data_key):
        return
    try:
        data = json.loads(redis.get(data_key).decode('utf-8'))
        redis.delete(data_key)
    except ValueError:
        return

    print("Consuming tag of type {}".format(data['tag_type']))

    if data['tag_type'] == 'pageview':
        process_pageview(data)

    if data['tag_type'] == 'add_to_cart':
        process_add_to_cart(data)

    if data['tag_type'] == 'remove_from_cart':
        process_remove_from_cart(data)

    if data['tag_type'] == 'purchase':
        process_purchase(data)

    return tag_id


def create_and_get_remarketing(user_id, store_id):
    remarketing = Remarketing.objects.filter(user_id=user_id, store_id=store_id).first()

    if not remarketing:
        remarketing = Remarketing()
        remarketing.user_id = user_id
        remarketing.store_id = store_id
        remarketing.total_purchased = 0
        remarketing.num_carted = 0
        remarketing.num_purchased = 0
        remarketing.num_seen = 0
        remarketing.save()
    return remarketing


def create_and_get_cart(user_id, store_id):
    cart = OpenCarts.objects.filter(user_id=user_id, store_id=store_id).first()

    if not cart:
        cart = OpenCarts()
        cart.user_id = user_id
        cart.store_id = store_id
        cart.timestamp = int(time())
        cart.save()
    return cart


def create_and_get_purchases(store_id, origin):
    purchase = OriginPurchases.objects.filter(origin=origin, store_id=store_id).first()

    if not purchase:
        purchase = OriginPurchases()
        purchase.store_id = store_id
        purchase.origin = origin
        purchase.total_purchased = 0
        purchase.save()
    return purchase


def process_pageview(data):
    remarketing = create_and_get_remarketing(data['user_id'], data['store_id'])
    seen_skus = remarketing.products_seen.keys()

    if data['pagetype'] == 'product':
        for product in data['products']:
            remarketing.num_seen += 1
            if 'sku' in product.keys() and product['sku'] not in seen_skus:
                remarketing.products_seen[product['sku']] = product
                remarketing.products_seen[product['sku']]['times'] = 1
            else:
                remarketing.products_seen[product['sku']]['times'] += 1
    remarketing.save()


def process_add_to_cart(data):
    remarketing = create_and_get_remarketing(data['user_id'], data['store_id'])
    cart = create_and_get_cart(data['user_id'], data['store_id'])
    cart_skus = [p['sku'] for p in cart.cart if 'sku' in p.keys()]
    rmkt_skus = remarketing.products_carted.keys()

    for product in data['products']:
        remarketing.num_carted += 1
        if 'sku' in product.keys():
            if product['sku'] not in rmkt_skus:
                remarketing.products_carted[product['sku']] = product
                remarketing.products_carted[product['sku']]['times'] = 1
            else:
                remarketing.products_carted[product['sku']]['times'] += 1
            if product['sku'] not in cart_skus:
                cart.cart.append(product)
                cart.timestamp = int(time())

    remarketing.save()
    cart.save()


def process_remove_from_cart(data):
    cart = create_and_get_cart(data['user_id'], data['store_id'])

    for product in data['products']:
        if 'sku' in product.keys():
            cart.update(pull__cart__sku=product['sku'])
    cart.save()


def process_purchase(data):
    remarketing = create_and_get_remarketing(data['user_id'], data['store_id'])
    cart = create_and_get_cart(data['user_id'], data['store_id'])
    purchase = create_and_get_purchases(data['store_id'], data['origin'])
    rmkt_skus = remarketing.products_purchased.keys()

    for product in data['products']:
        remarketing.num_purchased += 1
        if 'sku' in product.keys() and product['sku'] not in rmkt_skus:
            remarketing.products_purchased[product['sku']] = product
            remarketing.products_purchased[product['sku']]['times'] = 1
        else:
            remarketing.products_purchased[product['sku']]['times'] += 1

    purchase.total_purchased += data['total']
    remarketing.total_purchased += data['total']
    purchase.transaction_ids.append(data['transaction_id'])

    remarketing.save()
    cart.delete()
    purchase.save()


if __name__ == '__main__':
    for i in range(10000):
        processed = get_next_tag()

        if processed is None:
            break
