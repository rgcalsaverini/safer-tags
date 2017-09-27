from time import time

import mongoengine as me
from mongoengine import LongField
from mongoengine.base.datastructures import BaseDict, BaseList


class BaseModel(object):
    def to_dict(self):
        valid_types = [str, list, dict, float, bool, int, BaseDict, BaseList, LongField]
        invalid_names = ['STRICT']

        if 'timestamp' in dir(self):
            self.age_hours = (time() - self.timestamp) / 3600

        return {k: getattr(self, k) for k in dir(self) if
                k[0] != '_' and type(getattr(self, k)) in valid_types and k not in invalid_names}


class StoreAffiliate(me.Document, BaseModel):
    store_id = me.StringField()
    url = me.StringField()


class Remarketing(me.Document, BaseModel):
    user_id = me.StringField()
    store_id = me.StringField()
    products_seen = me.DictField()
    num_seen = me.IntField()
    products_carted = me.DictField()
    num_carted = me.IntField()
    products_purchased = me.DictField()
    num_purchased = me.IntField()
    total_purchased = me.FloatField()


class OpenCarts(me.Document, BaseModel):
    user_id = me.StringField()
    store_id = me.StringField()
    cart = me.ListField()
    timestamp = me.LongField()


class OriginPurchases(me.Document, BaseModel):
    store_id = me.StringField()
    origin = me.StringField()
    total_purchased = me.FloatField()
    transaction_ids = me.ListField()
