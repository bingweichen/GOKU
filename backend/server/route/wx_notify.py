# -*- coding: UTF-8 -*-
"""
@author: bingwei
@time: 8/10/17
@desc: virtual card route
"""

from flask import Blueprint
from flask import jsonify
from flask import request

PREFIX = '/wx_notify'

wx_notify_app = Blueprint("wx_notify", __name__, url_prefix=PREFIX)


@wx_notify_app.route('', methods=['GET'])
def wx_notify():
    args = request.args
    data = request.get_json()
    print("args", args)
    print("data", data)
    return jsonify({
        "return_code": "SUCCESS",
        "return_msg": "OK"
    })


@wx_notify_app.route('/fb50a3de-97ba-11e7-836f-f45c89', methods=['GET'])
def wx_notify_1():
    args = request.args
    data = request.get_json()
    print("1")
    print("args", args)
    print("data", data)
    return jsonify({
        "return_code": "SUCCESS",
        "return_msg": "OK"
    })
