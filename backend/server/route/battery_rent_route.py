# -*- coding: UTF-8 -*-
"""
@author: larry.shuoren@outlook.com
@author: bingweiChen

@time: 8/10/17
@desc: battery rent route
"""

from flask import Blueprint
from flask import jsonify
from flask import request

from flask_jwt_extended import jwt_required, get_jwt_identity
from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist

from server.service import battery_rent_service
from server.utility.exception import *

# from server.utility.json_utility import models_to_json

PREFIX = '/battery_rent'

battery_rent = Blueprint("battery_rent", __name__, url_prefix=PREFIX)


# ***************************** 查询 ***************************** #
# 1. 扫一扫获取闪充信息
@battery_rent.route('/battery/<string:serial_number>', methods=['GET'])
# @jwt_required
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
            'response': {
                "error": '%s: %s' % (str(DoesNotExist), e.args),
                "message": '%s' % e.args
            }
        }), 400


# 2. 获取用户现有 闪充电池
@battery_rent.route('/battery', methods=['GET'])
@jwt_required
def get_user_battery():
    username = get_jwt_identity()
    # username = request.args.get("username")
    try:
        battery, battery_record = battery_rent_service.get_user_battery(
            username=username
        )
        # battery = model_to_dict(battery)
        # battery_record = model_to_dict(battery_record)
        battery = {
            "serial_number": battery.serial_number,
            "rent_date": battery_record.rent_date
        }
        return jsonify({
            'response': {
                "battery": battery,
                # "battery_record": battery_record
            }
        }), 200
    except DoesNotExist as e:
        return jsonify({
            'response': {
                "battery": [],
            }
        }), 200
        # return jsonify({
        #     'response': {
        #         'error': e.args,
        #         'message': '无租用电池'
        #     }
        # }), 400


# 3. 租用电池
@battery_rent.route('/rent', methods=['POST'])
@jwt_required
def rent_battery():
    """
    modify the user of e-bike

    eg = {
    # "username": "bingwei",
    "serial_number": "A00001"
    }

    :return:
    """
    username = get_jwt_identity()
    data = request.get_json()
    try:
        modified = battery_rent_service.rent_battery(
            username=username,
            serial_number=data["serial_number"]
        )
        return jsonify({'response': modified}), 200
    except DoesNotExist as e:
        return jsonify({
            'response': {
                'error': e.args,
                'message': '未开通虚拟消费卡'
            }
        }), 400
    except Error as e:
        return jsonify(
            {'response': {
                'error': '%s' % e.args,
                'message': '%s' % e.args
            }}), 400


# 4. 归还电池
@battery_rent.route('/return', methods=['POST'])
@jwt_required
def return_battery():
    """
    eg = {
    "serial_number": "A00001"
    }

    :return:
    :rtype:
    """
    username = get_jwt_identity()
    data = request.get_json()
    try:
        batter_record = battery_rent_service.return_battery(
            username=username,
            serial_number=data["serial_number"]
        )
        return jsonify({
            'response': model_to_dict(batter_record, recurse=False)}), 200
    except Error as e:
        return jsonify({
            'response': '%s: %s' % (str(Error), e.args)}), 400


# 报修电池
@battery_rent.route('/battery_report', methods=['PUT'])
# @jwt_required
def add_repair_report():
    """
    report a battery repair requirement

    eg = {
    "serial_number": "A00001",
    }
    :return:
    """
    data = request.get_json()
    battery_report = battery_rent_service.add_repair_report(
        serial_number=data.pop("serial_number")
    )
    battery_report = model_to_dict(battery_report)
    return jsonify({'response': {
        "battery_report": battery_report
    }}), 200
