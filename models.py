import mongoengine as me
from mongoengine.base.datastructures import BaseDict, BaseList


class BaseModel(object):
    def to_dict(self):
        valid_types = [str, list, dict, float, bool, BaseDict, BaseList]
        invalid_names = ['STRICT']
        return {k: getattr(self, k) for k in dir(self) if
                k[0] != '_' and type(getattr(self, k)) in valid_types and k not in invalid_names}


class StoreAffiliate(me.Document, BaseModel):
    store_id = me.StringField()
    url = me.StringField()


class Remarketing(me.Document, BaseModel):
    user_id = me.StringField()
    store_id = me.StringField()
    products_seen = me.DictField()
    products_carted = me.DictField()
    products_purchased = me.DictField()
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
