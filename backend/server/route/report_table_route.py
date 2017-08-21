"""

@author: Bingwei Chen

@time: 8/4/17

@desc: report_table route

"""

from flask import Blueprint
from flask import jsonify
from flask import request

from playhouse.shortcuts import model_to_dict
from server.utility.json_utility import models_to_json
from server.service import report_table_service

PREFIX = '/report_table'

report_table_app = Blueprint("report_table_app", __name__, url_prefix=PREFIX)


@report_table_app.route('/', methods=['PUT'])
def add():
    """
    eg = {
    "username": "bingwei",
    "appointment": 17,
    "address": "",
    "comment": "",
    "phone": 111111,
    }

    :return:
    :rtype:
    """
    data = request.get_json()
    report_table = report_table_service.add(
        appointment=data.pop("appointment"),
        user=data.pop("username"),
        address=data.pop("address"),
        comment=data.pop("comment"),
        phone=data.pop("phone"),
    )
    # report_table = model_to_dict(report_table)
    # 过滤输出内容
    report_table = {
        "username": report_table.user.username,
        "appointment": report_table.appointment.id,
        "address": report_table.address,
        "comment": report_table.comment,
        "phone": report_table.phone,
        "date": report_table.date
    }
    return jsonify({'response': report_table}), 200


@report_table_app.route('/all', methods=['GET'])
def get_all():
    username = request.args.get("username")

    report_tables = report_table_service.get_all(
        user=username
    )

    report_tables = models_to_json(report_tables)
    for i in range(len(report_tables)):
        report_tables[i]["user"] = report_tables[i]["user"]["username"]
        report_tables[i]["appointment"].pop("user")
    return jsonify({'response': report_tables}), 200
