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


# @battery_rent.route('/<int:b_id>', methods=['GET'])
# def get_battery_rent_info(b_id):
#     """
#     get battery rent information
#     :param b_id: battery id
#     :return: information
#     """
#     # FIXME
#     info = battery_rent_service.get_battery_rent_info(b_id)
#     if info:
#         return jsonify({'response': info}), 200
#     else:
#         return jsonify({'response': 'No information found'}), 404


@battery_rent.route('/', methods=['POST'])
def modify_use_status():
    """
    modify the user of e-bike
    :return:
    """
    # b_id: battery id
    # owner: user
    data = request.get_json()
    modified = battery_rent_service.modify_use_status(data)
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


@battery_rent.route('/', methods=['PUT'])
def add_battery():
    """
    add a battery
    :return:
    """
    data = request.get_json()
    battery = battery_rent_service.add(**data)
    return jsonify({'response': battery}), 200
