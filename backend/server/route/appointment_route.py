# -*- coding: UTF-8 -*-
"""

@author: Bingwei Chen

@time: 8/4/17

@desc: appointment route

1. appointment Add/Get/Modify/Remove

2. modify_appointment_status
"""
from flask import Blueprint
from flask import jsonify
from flask import request

from server.service import appointment_service

PREFIX = '/appointment'

appointment_app = Blueprint("appointment_app", __name__, url_prefix=PREFIX)


# ***************************** appointment ***************************** #
# 代码添加 完成
# 代码测试 完成
@appointment_app.route('/appointment', methods=['PUT'])  # test complete
def add_appointment():
    data = request.get_json()
    appointment = appointment_service.add(**data)
    if appointment:
        return jsonify({'response': appointment}), 200
    pass


@appointment_app.route('/appointment', methods=['GET'])
@appointment_app.route('/appointment/<string:appointment_id>',
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


@appointment_app.route('/appointment/<string:appointment_id>/<string:status>',
                       methods=['POST'])  # test complete
def modify_appointment_status(appointment_id, status):
    # data = request.get_json()
    # status = data
    result = appointment_service.modify_status(appointment_id, status)
    if result:
        return jsonify({'response': "modify success"}), 200
    else:
        return jsonify({'response': "no appointment find"}), 404
    pass


@appointment_app.route('/appointment/<string:appointment_id>',
                       methods=['DELETE'])  # test complete
def remove_appointment(appointment_id):
    result = appointment_service.remove_by_id(appointment_id)
    if result:
        return jsonify({'response': "delete success"}), 200
    else:
        return jsonify({'response': "no appointment find"}), 404
    pass


# ***************************** unit test ***************************** #
