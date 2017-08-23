# -*- coding: UTF-8 -*-
"""
@author: larry.shuoren@outlook.com
@time: 8/16/17
@desc: 订单管理

"""

from flask import Blueprint
from flask import jsonify
from flask import request

from server.service import appointment_service

from server.utility.json_utility import models_to_json
from server.utility.constant.basic_constant import *
PREFIX = '/manager/appointment_setting'

appointment_setting = Blueprint(
    "appointment_setting", __name__, url_prefix=PREFIX)


# ***************************** 查询 ***************************** #
# 查询所有订单 (分页）
@appointment_setting.route('/appointments/all/', methods=['GET'])
def get_appointments():
    page = request.args.get("page")
    paginate_by = request.args.get("paginate_by")
    appointments = appointment_service.get_all_paginate(
        int(page),
        int(paginate_by)
    )


    return jsonify({
        'response': {
            "appointments": models_to_json(appointments)
        }}), 200


# 查询租车或买车订单
@appointment_setting.route('/appointments/', methods=['GET'])
def get_appointment_by_type():
    """

    eg = ?appointment_type=租车&period=7&page=1&paginate_by=3

    # 如果想集成一个，获取所有使用 in ["租车"，"买车"]
    :return:
    :rtype:
    """
    appointment_type = request.args.get("appointment_type")
    period = request.args.get("period")

    appointments = appointment_service.manager_get(
        type=appointment_type,
        period=int(period),
        page=int(request.args.get("page")),
        paginate_by=int(request.args.get("paginate_by"))
    )
    return jsonify({
        'response': {
            "appointments": models_to_json(appointments)
        }}), 200


# 查询订单数量
@appointment_setting.route('/appointments/count', methods=['GET'])
def count_appointments():
    # appointment_type = request.args.get("appointment_type")
    count = appointment_service.count()
    return jsonify({
        'response': {
            "count": count
        }}), 200


# ***************************** 操作 ***************************** #
# 用户还车，由管理员执行，（到期日前还车成功）
@appointment_setting.route('/appointment/return_e_bike', methods=['POST'])
def return_e_bike():
    """

    eg = {
    "appointment_id": 1,
    "serial_number": "A00001"
    }
    :return:
    :rtype:
    """
    data = request.get_json()
    try:
        result = appointment_service.return_e_bike(
            appointment_id=data["appointment_id"],
            serial_number=data["serial_number"],

            account=data.pop("account"),
            account_type=data.pop("account_type"),
            comment=data.pop("comment")
        )
        if result:
            return jsonify({'response': result}), 200
    except Exception as e:
        return jsonify(
            {'response': '%s: %s' % (str(Exception), e.args)}), 400


# 更改订单状态
@appointment_setting.route(
    '/modify_status/<string:appointment_id>/<string:status>', methods=['POST'])
def modify_appointment_status(appointment_id, status):
    """
    eg = 1/已完成

    :param appointment_id:
    :type appointment_id:
    :param status:
    :type status:
    :return:
    :rtype:
    """
    result = appointment_service.modify_status(appointment_id, status)
    if result:
        return jsonify({'response': "modify success"}), 200
    else:
        return jsonify({'response': "no appointment find"}), 404


# 删除订单
@appointment_setting.route('/<string:appointment_id>', methods=['DELETE'])
def remove_appointment(appointment_id):
    result = appointment_service.remove_by_id(appointment_id)
    if result:
        return jsonify({'response': "delete success"}), 200
    else:
        return jsonify({'response': "no appointment find"}), 404


# 获取订单状态 对应表
@appointment_setting.route('/appointments/status', methods=['GET'])
def get_appointment_status_list():
    return jsonify({'response': {
        "buy": APPOINTMENT_STATUS,
        "rent": RENT_APPOINTMENT_STATUS
    }}), 200
