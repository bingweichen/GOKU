"""
@author: Bingwei Chen

@time: 8/4/17

@desc: 管理员

个人中心查询、

闪充使用情况（在使用闪充显示使用编号、没有使用闪充就显示未使用闪充）、
共享电动车的访问记录（记录访问时间)

? 个人中心全部都查看个人内容吗
？ 先暂时给所有人的表格吧
"""
from flask import Blueprint
from flask import jsonify
from flask import request

from playhouse.shortcuts import model_to_dict
from server.utility.json_utility import models_to_json

from server.service import user_service
from server.service import appointment_service
from server.service import refund_table_service
from server.service import report_table_service
from server.service import virtual_card_service
from server.service import battery_record_service
from server.service import battery_rent_service

PREFIX = '/manager/user_setting'

user_setting = Blueprint("user_setting", __name__, url_prefix=PREFIX)


# ***************************** 查看用户 ***************************** #
# 获取所有用户
@user_setting.route('/users/all', methods=['GET'])
def get_appointments():
    users = user_service.get_all()
    users = models_to_json(users, recurse=False)
    for i in range(len(users)):
        users[i].pop("password")
    return jsonify({
        'response': {
            "users": users
        }}), 200


# ***************************** 个人订单 ***************************** #
# 获取用户的订单情况
@user_setting.route('/user/appointment', methods=['GET'])
def get_user_appointment():
    username = request.args.get("username")
    appointments = appointment_service.get_all(username=username)
    appointments = models_to_json(appointments, recurse=False)
    return jsonify({
        'response': {
            "appointments": appointments
        }}), 200


# ***************************** 个人消费记录 ***************************** #
@user_setting.route('/consume_record', methods=['GET'])
def get_consume_record():
    """
    get consume records
    :param card_no: card number
    :return: consume records
    """
    username = request.args.get("username")
    record = virtual_card_service.get_consume_record(
        card_no=username
    )
    if record:
        return jsonify({'response': models_to_json(record, recurse=False)}), 200
    else:
        return jsonify({'response': 'No record found'}), 404


# ***************************** 个人退款 ***************************** #
@user_setting.route('/refund_table', methods=['GET'])
def get_refund_table():
    username = request.args.get("username")
    refund_tables = refund_table_service.get_all(username)
    return jsonify({
        'response': {
            "refund_tables": models_to_json(refund_tables, recurse=False)
        }}), 200


# ***************************** 个人电动车报修 ***************************** #
@user_setting.route('/report_table', methods=['GET'])
def get_report_table():
    username = request.args.get("username")
    report_tables = report_table_service.get_all(
        user=username
    )
    report_tables = models_to_json(report_tables, recurse=False)
    return jsonify({'response': report_tables}), 200


# ***************************** 个人闪充记录 ***************************** #
@user_setting.route('/battery_record', methods=['GET'])
def get_battery_record():
    username = request.args.get("username")
    battery_record = battery_record_service.get_all(
        username=username
    )
    battery_record = models_to_json(battery_record)
    return jsonify({'response': battery_record}), 200


# ***************************** 个人现在使用的闪充 ***************************** #
@user_setting.route('/on_load_battery', methods=['GET'])
def get_on_load_battery():
    username = request.args.get("username")
    try:
        battery = battery_rent_service.get_on_load_battery(
            username=username
        )
        battery = model_to_dict(battery)
        return jsonify({'response': battery}), 200
    except Exception as e:
        return jsonify({'response': {
            "message": "没有正在使用的电池",
            "error": e.args,
        }}), 400
