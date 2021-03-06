import json
from flask import redirect, session
from functools import wraps
from db import USERS_FILE

with open(USERS_FILE) as users_file:
    g_users = json.load(users_file)

class User(object):
    def __init__(self, login):
        with open(USERS_FILE) as users_file:
            g_users = json.load(users_file)

        if login is not None and login in g_users:
            self.login = login
            self.anonymous = False
            self.password = g_users[login]["password"]
        else:
            self.anonymous = True

    def is_anonymous(self):
        return self.anonymous

    def is_authorized(self):
        return not self.anonymous


def authorize(login, password):
    user = User(login)
    if user.is_anonymous():
        return user
    if user.password == password:
        return user
    return User(None)

def get_user(login):
    return User(login)

def authorized(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        user = get_user(session.get("user_login", None))
        if user.is_authorized():
            return fn(*args, **kwargs)
        else:
            return redirect('/')
    return wrapped

def not_authorized(fn):
    @wraps(fn)
    def wrapped():
        user = get_user(session.get("user_login", None))
        if user.is_authorized():
            return redirect('/menu')
        else:
            return fn()
    return wrapped

    
