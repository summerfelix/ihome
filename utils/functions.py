from functools import wraps

from flask import session, jsonify, redirect, url_for

from app.models import User
from utils import status_code


def get_sqlalchemy_uri(DATABASE):
    user = DATABASE['USER']
    password = DATABASE['PASSWORD']
    host = DATABASE['HOST']
    port = DATABASE['PORT']
    name = DATABASE['NAME']
    engine = DATABASE['ENGINE']
    driver = DATABASE['DRIVER']
    return f'{engine}+{driver}://{user}:{password}@{host}:{port}/{name}'


def login_status(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            user_id = session['user_id']
        except:
            # return jsonify(status_code.LOGIN_STATUS_NOT_LOGIN)
            return redirect(url_for('user.login'))
        user = User.query.filter(User.id == user_id).first()
        if not user:
            # return jsonify(status_code.LOGIN_STATUS_NOT_LOGIN)
            return redirect(url_for('user.login'))
        return func(*args, **kwargs)
    return inner

