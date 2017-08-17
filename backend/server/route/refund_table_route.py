"""

@author: Bingwei Chen

@time: 8/4/17

@desc: 管理员

电动车售卖价格设置
"""

from flask import Blueprint
from flask import jsonify
from flask import request

from playhouse.shortcuts import model_to_dict

from server.service import refund_table_service
from server.utility.json_utility import models_to_json

PREFIX = '/refund_table'

refund_table = Blueprint("refund_table", __name__, url_prefix=PREFIX)


# 获取所有退款记录
@refund_table.route('/', methods=['GET'])
def get_appointments():
    username = request.args.get("username")
    refund_tables = refund_table_service.get_all(username)
    return jsonify({
        'response': {
            "appointments": models_to_json(refund_tables)
        }}), 200
