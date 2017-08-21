# -*- coding: UTF-8 -*-
"""
@author: larry.shuoren@outlook.com
@time: 8/9/17
@desc: e-bike rent route

# 暂时不用
"""

from flask import Blueprint
from flask import jsonify
from flask import request

from server.service import e_bike_rent_service

PREFIX = '/e_bike_rent'

e_bike_rent = Blueprint("e_bike_rent", __name__, url_prefix=PREFIX)


@e_bike_rent.route('', methods=['PUT'])
def add_e_bike():
    """
    add e-bike to database
    :return:
    """
    data = request.get_json()
    e_bike = e_bike_rent_service.add(**data)
    return jsonify({'response': e_bike}), 200


@e_bike_rent.route('', methods=['POST'])
def modify_user():
    """
    modify user of e-bike
    :return:
    """
    data = request.get_json()
    result = e_bike_rent_service.modify_user(data)
    if result:
        return jsonify({'response': "modify success"}), 200
    else:
        return jsonify({'response': "no e_bike_model find"}), 404


@e_bike_rent.route('', method=['GET'])
def get_available_e_bike_models():
    """
    get available e-bike models
    :return: available e-bike models
    """
    e_bikes = e_bike_rent_service.get_available_e_bike_models()
    if e_bikes:
        return jsonify({"response": e_bikes}), 200
    else:
        return jsonify({"response": "No e-bike found"})


@e_bike_rent.route('/<string:name>', method=['GET'])
def get_e_bike_model_information(name):
    """
    get information of an e-bike model
    :param name: e-bike model name
    :return: information of an e-bike model
    """
    info = e_bike_rent_service.get_e_bike_model_information(name)
    if info:
        return jsonify({"response": info}), 200
    else:
        return jsonify({"response": "No information found"})


@e_bike_rent.route('/<string:name>/<string:color>', method=['GET'])
def get_storage(name, color):
    """
    get storage of a certain e-bike model with a certain color
    :param name: e-bike model
    :param color: color
    :return: storage
    """
    storage = e_bike_rent_service.get_storage(name, color)
    if storage:
        return jsonify({"response": storage}), 200
    else:
        return jsonify({"response": "No storage"})
