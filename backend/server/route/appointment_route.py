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

from server.service import appointment_service
from server.utility.exception import NoStorageError

PREFIX = '/appointment'

appointment_app = Blueprint("appointment_app", __name__, url_prefix=PREFIX)


# ***************************** appointment ***************************** #
# 1.提交预约单
@appointment_app.route('/', methods=['PUT'])
def add_appointment():
    try:
        data = request.get_json()
        appointment = appointment_service.add_appointment(**data)
        if appointment:
            return jsonify({'response': appointment}), 200

    except NoStorageError as e:
        return jsonify(
            {'response': '%s: %s' % (str(NoStorageError), e.args)}), 400
        # return jsonify({'response': str(NoStorageError)}), 400


# 2. 提交预约款付款成功
@appointment_app.route('/status/appointment_payment_success', methods=['POST'])
def appointment_payment_success():
    data = request.get_json()
    appointment_id = data["appointment_id"]
    result = appointment_service.appointment_payment_success(appointment_id)
    if result:
        return jsonify({'response': result}), 200


# 3. 提交取车码
@appointment_app.route('/status/upload_code', methods=['POST'])
def upload_code():
    data = request.get_json()
    appointment_id = data["appointment_id"]
    code = data["code"]
    result = appointment_service.upload_code(appointment_id, code)
    if result:
        return jsonify({'response': result}), 200


# 4. 提交付款成功
@appointment_app.route('/status/total_payment_success', methods=['POST'])
def total_payment_success():
    data = request.get_json()
    appointment_id = data["appointment_id"]
    result = appointment_service.total_payment_success(appointment_id)
    if result:
        return jsonify({'response': result}), 200


# 取消订单
@appointment_app.route('/status/cancel', methods=['POST'])
def cancel_appointment():
    data = request.get_json()
    appointment_id = data["appointment_id"]
    result = appointment_service.cancel_appointment(appointment_id)


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

# ***************************** unit test ***************************** #
# 生成预约单
# localhost:5000/appointment  PUT
# json = {
#     "user": "bingwei",
#     "e_bike_model": "E101小龟",
#     "color": "蓝",
#     "type": "小龟",
#     "date": datetime.now(),
#     "note": "xx"
# }
