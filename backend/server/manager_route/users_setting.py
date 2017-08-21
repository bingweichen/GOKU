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


PREFIX = '/manager/user_setting'

user_setting = Blueprint("user_setting", __name__, url_prefix=PREFIX)


# ***************************** 个人中心 ***************************** #
# 获取所有用户
@user_setting.route('/users', methods=['GET'])
def get_appointments():
    users = user_service.get_all()
    users = models_to_json(users)
    return jsonify({
        'response': {
            "users": users
        }}), 200


# 订单查询（买车、租车情况、(某个人的订单)。。。
# 获取用户的订单情况
@user_setting.route('/user/appointment', methods=['GET'])
def get_user_appointment():
    username = request.args.get()
    appointments = appointment_service.get_all(username=username)
    appointments = models_to_json(appointments)
    return jsonify({
        'response': {
            "appointments": appointments
        }}), 200


# # ***************************** 退款表 ***************************** #
# # 获取所有退款记录
# @user_setting.route('/refund_table', methods=['GET'])
# def get_refund_table():
#     refund_tables = refund_table_service.get_all()
#     refund_tables = models_to_json(refund_tables)
#     return jsonify({
#         'response': {
#             "refund_tables": refund_tables
#         }}), 200
#
#
# # 确认退款
# @user_setting.route('/refund_table/status', methods=['POST'])
# def modify_refund_table_status():
#     data = request.get_json()
#     result = refund_table_service.modify_status(
#         refund_table_id=data.pop("refund_table_id"),
#         status="已退款"
#     )
#     return jsonify({
#         'response': {
#             "result": result
#         }}), 200
#
#
# # 售后维修记录等）、
# # ***************************** 报修表 ***************************** #
# @user_setting.route('/report_table', methods=['GET'])
# def get_report_table():
#     report_table = report_table_service.get_all()
#     report_table = models_to_json(report_table)
#     return jsonify({
#         'response': {
#             "report_table": report_table
#         }}), 200

