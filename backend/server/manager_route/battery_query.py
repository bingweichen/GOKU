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

PREFIX = '/manager//battery_query'

battery_query = Blueprint("battery_query", __name__, url_prefix=PREFIX)


# 使用闪充的总人数
@battery_query.route('/total_use', methods=['GET'])
def get_total_uses_amount():
    count = battery_rent_service.manager_get_total_uses_amount()
    return jsonify({
        'response': {
            "total_use": count
        }}), 200


# 正在使用人数
@battery_query.route('/current_use', methods=['GET'])
def get_current_uses_amount():
    count = battery_rent_service.manager_get_current_uses_amount()
    return jsonify({
        'response': {
            "current_use": count
        }}), 200


# 输入闪充编号查询，查询闪充电池的使用状态和用户信息
@battery_query.route('/use_status/<string:serial_number>', methods=['GET'])
def get_use_status_by_id(serial_number):
    result = battery_rent_service.manager_get_use_status_by_id(serial_number)
    return jsonify({
        'response': {
            "use_status": result
        }}), 200


# 可查询历史记录：一周内、一月内、三个月内。
@battery_query.route(
    '/history_record/<string:serial_number>/<int:days>', methods=['GET'])
def get_history_record_by_id(serial_number, days):
    result = battery_rent_service.manager_get_history_record_by_id(serial_number, days)
    return jsonify({
        'response': {
            "history_record": models_to_json(result)
        }}), 200
