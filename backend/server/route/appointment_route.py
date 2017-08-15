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
from server.utility.exception import NoStorageError, WrongSerialsNumber

PREFIX = '/appointment'

appointment_app = Blueprint("appointment_app", __name__, url_prefix=PREFIX)


# ***************************** buy appointment ***************************** #
# 1.提交生成 预约单
@appointment_app.route('/', methods=['PUT'])
def add_appointment():
    """
    买车订单
    e_bike_model: string
    color: string
    category: string

    eg = {
    "e_bike_model": "小龟电动车 爆款 48V、12A",
    "color": "蓝",
    "category": "小龟"
    }

    :return: the appointment created
    :rtype: json
    """
    username = "bingwei"
    data = request.get_json()
    try:
        appointment = appointment_service.add_appointment(
            user=username,
            **data
        )
        if appointment:
            return jsonify({'response': model_to_dict(appointment)}), 200

    except NoStorageError as e:
        return jsonify(
            {'response': '%s: %s' % (str(NoStorageError), e.args)}), 400
        # return jsonify({'response': str(NoStorageError)}), 400


# 2. 提交预约款付款成功
@appointment_app.route('/status/appointment_payment_success', methods=['POST'])
def appointment_payment_success():
    """
    appointment_id: string

    :return: 1 for success
    :rtype: int
    """
    data = request.get_json()
    appointment_id = data["appointment_id"]
    result = appointment_service.appointment_payment_success(appointment_id)
    if result:
        return jsonify({'response': result}), 200


# 3. 提交取车码
@appointment_app.route('/check/upload_serials_number', methods=['POST'])
def upload_code():
    """
    appointment_id: int
    serials_number: string

    eg = {
    "appointment_id": 3,
    "serials_number": "AM0002"
    }

    :return: 1 for success
    :rtype:
    """
    data = request.get_json()
    appointment_id = data["appointment_id"]
    serials_number = data["serials_number"]
    try:
        result = appointment_service.upload_serial_number(
            appointment_id, serials_number)
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
    "appointment_id": 3,
    }
    :return: 1 for success
    :rtype:
    """
    data = request.get_json()
    appointment_id = data["appointment_id"]
    result = appointment_service.total_payment_success(appointment_id)
    if result:
        return jsonify({'response': result}), 200


# 5. 针对租车 到期日前还车成功， 由管理员发起


# 取消订单
@appointment_app.route('/status/cancel', methods=['POST'])
def cancel_appointment():
    """
    appointment_id: int

    eg = {
    "appointment_id": 3,
    }
    :return: 1 for success
    :rtype:
    """
    data = request.get_json()
    appointment_id = data["appointment_id"]
    result = appointment_service.cancel_appointment(appointment_id)
    if result:
        return jsonify({'response': result}), 200


@appointment_app.route('/', methods=['GET'])
@appointment_app.route('/<string:appointment_id>',
                       methods=['GET'])  # test complete
def get_appointment(appointment_id=None):
    if appointment_id is None:
        appointments = appointment_service.get_all()
    else:
        appointments = [appointment_service.get_by_id(appointment_id)]
    if appointments:
        return jsonify({'response': {"appointments": appointments}}), 200
    else:
        return jsonify({'response': "no appointment find"}), 404
    pass


# ***************************** rent appointment ***************************** #
# 1.提交生成 预约单
@appointment_app.route('/rent/', methods=['PUT'])
def add_rent_appointment():
    """
    租车订单
    eg = {
    "e_bike_model": "租车 闪租 48V、20A",
    "color": "蓝",
    "category": "租车",
    "rent_time_period": "学期"

    }

    :return: the appointment created
    :rtype: json
    """
    pass

    username = "bingwei"
    data = request.get_json()
    try:
        appointment = appointment_service.add_rent_appointment(
            user=username,
            e_bike_model=data.pop("e_bike_model"),
            color=data.pop("color"),
            category=data.pop("category"),
            rent_time_period=data.pop("rent_time_period"),
            **data
        )
        if appointment:
            return jsonify({'response': model_to_dict(appointment)}), 200

    except NoStorageError as e:
        return jsonify(
            {'response': '%s: %s' % (str(NoStorageError), e.args)}), 400


# # 用户还车，由管理员执行
# @appointment_app.route('/rent/return_e_bike', methods=['POST'])
# def return_e_bike():
#     data = request.get_json()
#     try:
#         appointment = appointment_service.


# ***************************** unit test ***************************** #
# 更改预约单状态
@appointment_app.route('/modify_status/<string:appointment_id>/<string:status>',
                       methods=['POST'])
def modify_appointment_status(appointment_id, status):
    # data = request.get_json()
    # status = data
    result = appointment_service.modify_status(appointment_id, status)
    if result:
        return jsonify({'response': "modify success"}), 200
    else:
        return jsonify({'response': "no appointment find"}), 404
    pass


@appointment_app.route('/<string:appointment_id>',
                       methods=['DELETE'])  # test complete
def remove_appointment(appointment_id):
    result = appointment_service.remove_by_id(appointment_id)
    if result:
        return jsonify({'response': "delete success"}), 200
    else:
        return jsonify({'response': "no appointment find"}), 404
    pass
