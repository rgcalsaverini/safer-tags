from time import time
from uuid import uuid4

from flask import session


def generate_user_id():
    """
    Generates an unique user ID, based on a large random portion and a timestamp.
    :return: A unique user ID
    """
    time_bit = hex(int(time() * 10000000))[2:]
    return uuid4().hex + time_bit


def identify_user():
    """
    Attaches an unique user ID on not yet identified users. It could be easily improved to
    enable cross-device by associating uid's with hashed emails, and crosschecking that table.
    :return:
    """
    if 'user_id' not in session.keys():
        session['user_id'] = generate_user_id()