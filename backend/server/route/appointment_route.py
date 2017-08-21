# -*- coding: UTF-8 -*-
"""

@author: Bingwei Chen

@time: 8/4/17

@desc: appointment route

1. appointment Add/Get/Modify/Remove

2. modify_appointment_status

1. 生成订单 未预约付款（等待付预约款）
2. 付款预约款后更改状态 （等待提货）
3. 输入提车码后 (等待付款)
4. 付款后(交易成功）
"""
from flask import Blueprint
from flask import jsonify
from flask import request

from playhouse.shortcuts import model_to_dict

from server.service import appointment_service
from server.utility.exception import NoStorageError, WrongSerialsNumber, Error
from server.utility.json_utility import models_to_json

PREFIX = '/appointment'

appointment_app = Blueprint("appointment_app", __name__, url_prefix=PREFIX)


# ***************************** get ***************************** #
@appointment_app.route('/all', methods=['GET'])
def get_all_appointments():
    username = request.args.get('username')
    appointments = appointment_service.get_all(username)
    return jsonify({
        'response': {
            "appointments": models_to_json(appointments)
        }}), 200


@appointment_app.route('', methods=['GET'])
def get_appointment():
    username = request.args.get('username')
    appointment_id = request.args.get('appointment_id')
    appointment = appointment_service.get_by_id(
        appointment_id=appointment_id, username=username)
    return jsonify({
        'response': {
            "appointment": model_to_dict(appointment)}}), 200


# ************************** appointment procedure ********************** #
# 1.提交生成 预约单
@appointment_app.route('', methods=['PUT'])
def add_appointment():
    """
    买车订单
    e_bike_model: string
    color: string
    category: string

    eg = {
    "username" : "bingwei",

    "e_bike_model": "小龟电动车 爆款 48V、12A",
    "color": "蓝",
    "category": "小龟",
    "type": "买车",
    "note": "",
    "coupon": null

    }

    租车订单
    eg = {
    "username" : "Shuo_Ren",

    "e_bike_model": "闪租 48V、20A",
    "color": "黑",
    "category": "闪租",
    "type": "租车",
    "note": "",
    "coupon": null,

    "rent_time_period": "学期"
    }

    :return: the appointment created
    :rtype: json
    """
    data = request.get_json()
    try:
        appointment = appointment_service.add_appointment(
            user=data.pop("username"),
            **data
        )
        # TODO 内容筛选
        return jsonify({'response': model_to_dict(appointment)}), 200

    except Error as e:
        return jsonify(
            {'response': '%s: %s' % (str(Error), e.args)}), 400


# 2. 提交预约款付款成功
@appointment_app.route('/status/appointment_payment_success', methods=['POST'])
def appointment_payment_success():
    """
    appointment_id: string

    eg = {
    "username" : "bingwei",
    "appointment_id": 3
    }

    :return: 1 for success
    :rtype: int
    """
    data = request.get_json()
    result = appointment_service.appointment_payment_success(
        user=data.pop("username"),
        appointment_id=data.pop("appointment_id")
    )
    if result:
        return jsonify({'response': result}), 200


# 3. 检查取车码
@appointment_app.route('/check/upload_serials_number', methods=['POST'])
def upload_code():
    """
    appointment_id: int
    serials_number: string

    eg = {
    "username": "bingwei",
    "appointment_id": 3,
    "serial_number": "AM0002"
    }

    :return: 1 for success
    :rtype:
    """
    data = request.get_json()

    try:
        result = appointment_service.upload_serial_number(
            user=data.pop("username"),
            appointment_id=data.pop("appointment_id"),
            serial_number=data.pop("serial_number")
        )
        if result:
            return jsonify({'response': result}), 200
    except WrongSerialsNumber as e:
        return jsonify(
            {'response': '%s: %s' % (str(WrongSerialsNumber), e.args)}), 400


# 4. 提交付款成功
@appointment_app.route('/status/total_payment_success', methods=['POST'])
def total_payment_success():
    """
    appointment_id: int

    eg = {
    "username": "bingwei",
    "appointment_id": 3,
    }

    :return: 1 for success
    :rtype:
    """
    data = request.get_json()
    result = appointment_service.total_payment_success(
        user=data.pop("username"),
        appointment_id=data.pop("appointment_id"),
    )
    if result:
        return jsonify({'response': result}), 200


# 5. 取消订单
@appointment_app.route('/status/cancel', methods=['POST'])
def cancel_appointment():
    """
    appointment_id: int

    eg = {
    "username": "bingwei",
    "appointment_id": 3,
    "account": "BingweiChen",
    "account_type": "wechat",
    "comment": "test",

    }
    :return: 1 for success
    :rtype:
    """
    data = request.get_json()
    # appointment_id = data["appointment_id"]
    result = appointment_service.cancel_appointment(
        username=data.pop("username"),
        appointment_id=data.pop("appointment_id"),
        account=data.pop("account"),
        account_type=data.pop("account_type"),
        comment=data.pop("comment"),
        **data
    )
    if result:
        return jsonify({'response': result}), 200

# ***************************** unit test ***************************** #

