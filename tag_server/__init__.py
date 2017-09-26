import json
import random

import mongoengine as me
import redis
from flask import Flask
from flask_cors import CORS


def random_string(length, dictionary=None):
    """
    Generates a random string. Useful for an app's secret key.

    :param length: Final length of the generated string
    :param dictionary: String containing the available chars. Optional
    :return: The generated String
    """
    chars = list(dictionary or 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%&*() {}[]:?/\\|')
    return ''.join([random.choice(chars) for _ in range(length)])


def create_flask_app():
    """
    Creates a react application.

    :return: Flask app object
    """
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    random.seed('example_tag_server')
    app.secret_key = random_string(100)
    return app


def gen_error(error_id, *args):
    """
    Generate a HTTP error response from an error_id and optional arguments.

    :param error_id: The string identifier of the error
    :param args: Optional arguments, particular to every error_id, to be displayed on the description
    :return: a JSON error body and an appropriate HTTP status code
    """
    errors = {
        'generic': {'status': 400, 'error': 'generic', 'description': 'A unspecified error occurred'},
        'invalid_pagetype': {'status': 400, 'description': 'Invalid pagetype "{}"'},
    }

    if error_id in errors.keys():
        error = dict(**errors[error_id])
        error['description'] = error['description'].format(*args)
        error['error'] = error_id
        return json.dumps({**error, 'success': False}), error['status']

    return json.dumps(errors['generic']), errors['generic']['status']


def create_redis_connection(app=None):
    """
    Create a new redis connection and setup a few necessary registries
    :param app: A flask application object
    :return:
    """

    if app:
        app.logger.info('Instantiated new redis connection.')

    redis_connection = redis.StrictRedis(
        host="localhost",
        port=6379,
        db=0
    )

    if not redis_connection.exists('last_queue_idx'):
        redis_connection.set('last_queue_idx', 0)

    return redis_connection


def initiate_mongo_connection():
    me.connect('safer_tags')
