# -*- coding: UTF-8 -*-
"""
@author: larry.shuoren@outlook.com
@time: 8/10/17
@desc: battery rent route
"""

from flask import Blueprint
from flask import jsonify
from flask import request

from server.service import battery_rent_service

PREFIX = '/battery_rent'

battery_rent = Blueprint("battery_rent", __name__, url_prefix=PREFIX)


@battery_rent.route('/battery', methods=['PUT'])
def add_battery():
    """
    add a battery

    eg = {
    "desc": "xxx"
    }

    :return:
    """
    data = request.get_json()
    battery = battery_rent_service.add(**data)
    return jsonify({'response': battery}), 200


@battery_rent.route('/<string:serial_number>', methods=['GET'])
def get_battery_rent_info(serial_number):
    """
    get battery rent information

    :param serial_number: battery serial_number
    :return: information
    """
    # FIXME
    info = battery_rent_service.get_battery_rent_info(serial_number)
    if info:
        return jsonify({'response': info}), 200
    else:
        return jsonify({'response': 'No information found'}), 404


@battery_rent.route('/rent', methods=['POST'])
def rent_battery():
    """
    modify the user of e-bike
    :return:
    """
    # b_id: battery id
    # owner: user
    data = request.get_json()
    modified = battery_rent_service.modify_use_status(
        serial_number=data["serial_number"],
        username=data["username"]
    )
    return jsonify({'response': modified}), 200


@battery_rent.route('/', methods=['PUT'])
def add_repair_report():
    """
    report a battery repair requirement  
    :return:
    """
    # b_id: battery id
    # owner: user
    data = request.get_json()
    report = battery_rent_service.add_repair_report(data)
    return jsonify({'response': report}), 200


