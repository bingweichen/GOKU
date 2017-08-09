# -*- coding: UTF-8 -*-
"""
@author: Shuo Ren
@time: 8/9/17
@desc: flash rent route
"""

from flask import Blueprint
from flask import jsonify
from flask import request

from server.service import flash_rent_service

PREFIX = '/flash_rent'

flash_rent = Blueprint("flash_rent", __name__, url_prefix=PREFIX)


@flash_rent.route('/', methods=['GET'])
def get_e_bike_list():
    e_bikes = flash_rent_service.get_e_bike_list()
    if e_bikes:
        return jsonify({"response": e_bikes}), 200
    else:
        return jsonify({"response": "No e-bike found"})
