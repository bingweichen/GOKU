# -*- coding: UTF-8 -*-
"""
@author: larry.shuoren@outlook.com
@time: 8/16/17
@desc: appointment query route

电动车订单：
包括买车的订单和租车的订单，两个界面。
如果是买车的只是预约没有提车，显示已预约，提车完成显示已完成；
租车如果只是预约没有提车，显示已预约，提车完成显示已完成。
记录一天内订单、一周内订单、一个月和一年内订单查询，
能查询相应的订单数量和订单信息。
"""

from flask import Blueprint
from flask import jsonify
from flask import request

from server.service import appointment_service
from server.utility.json_utility import models_to_json

PREFIX = '/manager/appointment_query'

appointment_query = Blueprint("appointment_query", __name__, url_prefix=PREFIX)


# 所有
@appointment_query.route('/appointments/all', methods=['GET'])
def get_appointments():
    appointments = appointment_service.get_all()
    return jsonify({
        'response': {
            "appointments": models_to_json(appointments)
        }}), 200


# 如果想集成一个，获取所有使用 in ["租车"，"买车"]
# 租车，买车
@appointment_query.route('/appointments/', methods=['GET'])
def get_appointment_by_type():
    appointment_type = request.args.get("appointment_type")
    appointments = appointment_service.get_by_type(
        type=appointment_type
    )
    return jsonify({
        'response': {
            "appointments": models_to_json(appointments)
        }}), 200


# 订单数量
@appointment_query.route('/appointments/count', methods=['GET'])
def count_appointments():
    # appointment_type = request.args.get("appointment_type")
    count = appointment_service.count()
    return jsonify({
        'response': {
            "count": count
        }}), 200


