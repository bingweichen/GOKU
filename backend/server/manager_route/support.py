"""
@author: bingweiChen
@time: 8/10/17
@desc: support 售后服务

report_table， refund_table

点击售后服务：提供上门和实体维修，
填写维修信息后直接与客服联系或者支付上门佣金后拨打维修部的电话或者微信联系（售后服务设置参见5）。
设置填写维修故障填写网页、联系微信和维修部电话。
三个区域分开，显示最近的维修信息（各板块分开显示维修订单、人数，已接单和未接单），
历史记录：一天、一周、一月、三个月。

"""

from flask import Blueprint
from flask import jsonify
from flask import request

from server.service import report_table_service
from server.service import refund_table_service
from server.service import battery_report_service

from server.utility.json_utility import models_to_json
from playhouse.shortcuts import model_to_dict

PREFIX = '/manager/support'

support_app = Blueprint("support", __name__, url_prefix=PREFIX)


# ***************************** 报修表 ***************************** #
# 获取所有报修
@support_app.route('/report_table/all', methods=['GET'])
def get_all_report_table():
    report_tables = report_table_service.manager_get_all()
    report_tables = models_to_json(report_tables, recurse=False)
    # for i in range(len(report_tables)):
    #     report_tables[i]["user"] = report_tables[i]["user"]["username"]
    #     report_tables[i]["appointment"].pop("user")
    return jsonify({'response': report_tables}), 200


# 获取所有电池报修
@support_app.route('/battery_report/all', methods=['GET'])
def get_all_battery_report():
    battery_report = battery_report_service.get_all_paginate(
        # period=int(request.args.get("days"))
    )
    battery_report = models_to_json(battery_report, recurse=False)
    return jsonify({'response': battery_report}), 200


# ***************************** 退款表 ***************************** #
# 获取所有退款记录
@support_app.route('/refund_table/all', methods=['GET'])
def get_refund_table():
    refund_tables = refund_table_service.get_all()
    return jsonify({
        'response': {
            "refund_tables": models_to_json(refund_tables, recurse=False)
        }}), 200


# 更改退款记录状态
@support_app.route('/refund_table/set_success_refund_status', methods=['POST'])
def modify_refund_table():
    """

    eg = {
    "refund_table_id":
    }

    :return:
    :rtype:
    """
    data = request.get_json()
    result = refund_table_service.modify_status(
        refund_table_id=data.pop("refund_table_id"),
        status="已退款"
    )
    return jsonify({
        'response': {
            "result": result
        }}), 200
