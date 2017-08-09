# -*- coding: UTF-8 -*-
"""
@author: Shuo Ren
@time: 8/9/17
@desc: e-bike rent route
"""

from flask import Blueprint
from flask import jsonify
from flask import request

from server.service import e_bike_rent_service

PREFIX = '/e_bike_rent'

e_bike_rent = Blueprint("e_bike_rent", __name__, url_prefix=PREFIX)


@e_bike_rent.route('/', methods=['PUT'])
def add_e_bike():
    data = request.get_json()
    e_bike = e_bike_rent_service.add(**data)
    if e_bike:
        return jsonify({'response': e_bike}), 200


@e_bike_rent.route('/<int:plate_no>/<string:user>', methods=['POST'])
def add_e_bike(plate_no, user):
    result = e_bike_rent_service.modify_user(plate_no, user)
    if result:
        return jsonify({'response': "modify success"}), 200
    else:
        return jsonify({'response': "no e_bike_model find"}), 404


@e_bike_rent.route('/', method=['GET'])
def get_available_e_bike_models():
    e_bikes = e_bike_rent_service.get_available_e_bike_models()
    if e_bikes:
        return jsonify({"response": e_bikes}), 200
    else:
        return jsonify({"response": "No e-bike found"})


@e_bike_rent.route('/<string:name>', method=['GET'])
def get_e_bike_model_information(name):
    info = e_bike_rent_service.get_e_bike_model_information(name)
    if info:
        return jsonify({"response": info}), 200
    else:
        return jsonify({"response": "No information found"})
