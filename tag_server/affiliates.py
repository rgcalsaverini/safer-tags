import json

from models import StoreAffiliate


def get_affiliates():
    """
    Forms the affiliates factory.

    :return:
    """

    class AffiliatesFactory(object):
        @staticmethod
        def get_affiliates(store_id):
            """
            Get a list of affiliates and their URL for a given store
            :return:
            """
            affiliates = StoreAffiliate.objects.filter(store_id=store_id).all()
            return json.dumps([a.to_dict() for a in affiliates])

    return AffiliatesFactory
