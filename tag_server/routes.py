from tag_server.affiliates import get_affiliates
from tag_server.api import get_api
from tag_server.collectors import get_collectors
from tag_server.user_identification import identify_user


def register_endpoint(app, url, view, methods=None):
    """
    Registers an endpoint into the app.

    :param app: A flask application object
    :param url: An URL for the endpoint
    :param view: The endpoint view
    :param methods: List of HTTP methods allowed. Defaults fo ['GET', 'POST']
    :return: The final URL and description for the endpoint
    """
    route_methods = ['POST', 'GET'] if methods is None else methods

    app.add_url_rule(
        rule=url,
        endpoint=view.__name__,
        view_func=view,
        methods=route_methods
    )

    return '{} "{}"'.format(url.ljust(70), view.__doc__.split('\n')[1].strip())


def route_to_app(app, redis):
    """
    Routes all endpoints to the flask application
    :param app: The flask application object
    :param redis: The redis connection object
    :return: None
    """
    collectors = get_collectors(app_ref=app, redis_ref=redis)
    affiliates = get_affiliates()
    api = get_api()

    app.before_request(identify_user)

    urls = list()

    urls.append(register_endpoint(app, '/tag/pageview/<string:store_id>/<string:pagetype>', collectors.pageview))
    urls.append(register_endpoint(app, '/tag/add-to-cart/<string:store_id>', collectors.add_to_cart))
    urls.append(register_endpoint(app, '/tag/remove-from-cart/<string:store_id>', collectors.remove_from_cart))
    urls.append(register_endpoint(app, '/tag/purchase/<string:store_id>/<string:tr_id>/<int:total>', collectors.purchase))
    urls.append(register_endpoint(app, '/tag/get-affiliates/<string:store_id>', affiliates.get_affiliates))
    urls.append(register_endpoint(app, '/api/remarketing', api.get_remarketing, ['GET']))
    urls.append(register_endpoint(app, '/api/carts', api.get_open_carts, ['GET']))
    urls.append(register_endpoint(app, '/api/purchases', api.get_purchases, ['GET']))

    # Default 404 route that shows valid endpoints
    app.add_url_rule(
        rule='/<path:_>',
        endpoint='404_fallback',
        view_func=lambda _: ('Invalid path, try one of:\n\n' + '\n'.join(urls), 404, {'Content-Type': 'text-plain'}),
        methods=['POST', 'GET']
    )
