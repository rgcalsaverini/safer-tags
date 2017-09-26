from tag_server import create_flask_app, create_redis_connection, initiate_mongo_connection
from tag_server.routes import route_to_app

# localhost:5123/tag/pageview/123/product?products=[{"sku":"OS004655PTA"}]&origin=testads
# localhost:5123/tag/add-to-cart/123?products=[{"sku":"OS004655PTA"}]&origin=testads
# localhost:5123/tag/purchase/123/1/4099?products=[{"sku":"OS004655PTA"}]&origin=testads

app = create_flask_app()
redis = create_redis_connection(app)
route_to_app(app, redis)
initiate_mongo_connection()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5123)
