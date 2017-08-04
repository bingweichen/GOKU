# -*- coding: UTF-8 -*-
"""

@author: Bingwei Chen

@time: 2017.07.20

@desc: service for user

"""
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from server.database.model import User


def add(username, password, kwargs):
    """

    eg = {
    "username": "bingwei",
    "password": "123456",
    "name": "bing",
    "phone": "11",
    "school": "123",
    "status": "1",
    "student_id": "11"
    }

    :param username:
    :type username:
    :param password:
    :type password:
    :param kwargs:
    :type kwargs:
    :return:
    :rtype:
    """
    hashed_password = generate_password_hash(password)
    user = User(username=username, password=hashed_password, **kwargs)
    return user.save()


def add_user(username, password, kwargs):
    user = User(username=username, password=password, **kwargs)
    return user.save()


def get_users_list():
    users = User.select()
    for user in users:
        print(user.username)

# def authenticate(user_ID, password):
#     user = user_business.get_by_user_ID(user_ID)
#     if user and check_password_hash(user.password, password):
#         user.id = str(user.id)
#         return user
#     return False
