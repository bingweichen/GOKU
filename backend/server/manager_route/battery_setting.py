# -*- coding: UTF-8 -*-
"""
@author: larry.shuoren@outlook.com
@author: bingweiChen
@time: 8/10/17
@desc: battery query card route


，还有三个区域各个区域的总人数和正在使用人数。


"""

from flask import Blueprint
from flask import jsonify
from flask import request

from server.service import battery_rent_service

from server.utility.json_utility import models_to_json
from playhouse.shortcuts import model_to_dict

PREFIX = '/manager/battery_setting'

battery_setting = Blueprint("battery_setting", __name__, url_prefix=PREFIX)


# ***************************** 查询 ***************************** #
# 使用闪充的总人次
@battery_setting.route('/total_use', methods=['GET'])
def get_total_uses_amount():
    count = battery_rent_service.manager_get_total_uses_amount()
    return jsonify({
        'response': {
            "total_use": count
        }}), 200


# 正在使用人数
@battery_setting.route('/current_use', methods=['GET'])
def get_current_uses_amount():
    count = battery_rent_service.manager_get_current_uses_amount()
    return jsonify({
        'response': {
            "current_use": count
        }}), 200


# 输入闪充编号查询，查询闪充电池的使用状态和用户信息
@battery_setting.route('/use_status/<string:serial_number>', methods=['GET'])
def get_use_status_by_id(serial_number):
    battery = battery_rent_service.manager_get_battery(serial_number)

    battery = model_to_dict(battery, recurse=False)
    return jsonify({
        'response': {
            "battery": battery
        }}), 200


# 可查询历史记录：一周内、一月内、三个月内。
@battery_setting.route(
    '/history_record/<string:serial_number>/<int:days>', methods=['GET'])
def get_history_record_by_id(serial_number, days):
    records = battery_rent_service.manager_get_history_record_by_id(
        serial_number, days)
    records = models_to_json(records, recurse=False)
    return jsonify({
        'response': {
            "records": records
        }}), 200


# ***************************** 操作 ***************************** #
# 添加电池
@battery_setting.route('/battery', methods=['PUT'])
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
    battery = model_to_dict(battery)
    return jsonify({'response': battery}), 200