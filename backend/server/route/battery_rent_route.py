# -*- coding: UTF-8 -*-
"""
@author: larry.shuoren@outlook.com
@time: 8/10/17
@desc: battery rent route
"""

from flask import Blueprint
from flask import jsonify
from flask import request

from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist

from server.service import battery_rent_service
from server.utility.json_utility import models_to_json
from server.utility.exception import *

PREFIX = '/battery_rent'

battery_rent = Blueprint("battery_rent", __name__, url_prefix=PREFIX)


# ***************************** service ***************************** #
# 1. 扫一扫获取闪充信息
@battery_rent.route('/battery/<string:serial_number>', methods=['GET'])
def get_battery(serial_number):
    """
    get battery rent information

    :param serial_number: battery serial_number
    :return: information
    """
    try:
        battery = battery_rent_service.get_battery(serial_number)
        return jsonify({'response': model_to_dict(battery)}), 200
    except DoesNotExist as e:
        return jsonify({
            'response': '%s: %s' % (str(DoesNotExist), e.args)}), 400


# 2. 获取用户现有 闪充电池
@battery_rent.route('/battery', methods=['GET'])
def get_user_battery():
    username = request.args("username")
    try:
        battery = battery_rent_service.get_user_battery(
            username=username
        )
        return jsonify({'response': model_to_dict(battery)}), 200
    except DoesNotExist as e:
        return jsonify({
            'response': '%s: %s' % (str(DoesNotExist), e.args)}), 400


# 3. 租用电池
@battery_rent.route('/rent', methods=['POST'])
def rent_battery():
    """
    modify the user of e-bike
    :return:
    """
    # b_id: battery id
    # owner: user
    data = request.get_json()
    try:
        modified = battery_rent_service.rent_battery(
            username=data["username"],
            serial_number=data["serial_number"]
        )
        return jsonify({'response': modified}), 200
    except Error as e:
        return jsonify({
            'response': '%s: %s' % (str(Error), e.args)}), 400


# 4. 归还电池
@battery_rent.route('/return', methods=['POST'])
def return_battery():
    data = request.get_json()
    try:
        batter_record = battery_rent_service.return_battery(
            username=data["username"],
            serial_number=data["serial_number"]
        )
        return jsonify({
            'response': model_to_dict(batter_record)}), 200
    except Error as e:
        return jsonify({
            'response': '%s: %s' % (str(Error), e.args)}), 400


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


