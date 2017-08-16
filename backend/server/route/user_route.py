# -*- coding: UTF-8 -*-
"""

@author: Bingwei Chen

@time: 8/4/17

@desc: user route

1. user register
2. user login
"""

from flask import Blueprint
from flask import jsonify
from flask import request
from flask_jwt_extended import create_access_token

from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist
from server.service import user_service
from server.utility.exception import PasswordError

PREFIX = '/user'

user_app = Blueprint("user_app", __name__, url_prefix=PREFIX)


@user_app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.pop('username')
    password = data.pop('password')

    if username is None or password is None:
        return jsonify({'response': 'invalid user or password'}), 400

    try:
        added_user = user_service.add(
            username=username, password=password, **data)
        added_user = model_to_dict(added_user)
        added_user.pop('password')
        return jsonify({'response': added_user}), 200
    except Exception as e:
        return jsonify({'response': '%s: %s' % (str(Exception), e.args)}), 400


@user_app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    try:
        user = user_service.login(username, password)
        user = model_to_dict(user)
        user.pop('password')

        # Identity can be any data that is json serializable
        response = {
            'response': {
                'token': create_access_token(identity=user),
                'user': user}}
        return jsonify(response), 200

    except DoesNotExist as e:
        return jsonify({
            'response': '%s: %s' % (str(DoesNotExist), e.args)}), 400

    except PasswordError as e:
        return jsonify({'response': 'Bad username or password, %s' % e}), 400


@user_app.route('/virtual_card', methods=['PUT'])
def create_virtual_card():
    """

    eg = {
     card_no = "bingwei"
    }

    :return:
    :rtype:
    """
    data = request.get_json()
    card_no = data.pop("card_no")
    try:
        virtual_card = user_service.create_virtual_card(
            card_no=card_no, **data
        )
        return jsonify({'response': model_to_dict(virtual_card)}), 200
    except Exception as e:
        return jsonify({'response': '%s: %s' % (str(Exception), e.args)}), 400

