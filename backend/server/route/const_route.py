"""

@author: Bingwei Chen

@time: 8/4/17

@desc: const


"""
from flask import Blueprint
from flask import jsonify
from flask import request

from playhouse.shortcuts import model_to_dict

from server.database.model import Const
from server.service import const_service
from server.utility.json_utility import models_to_json
PREFIX = '/const'

const_app = Blueprint("const_app", __name__, url_prefix=PREFIX)


# 获取所有参数
@const_app.route('/', methods=['GET'])
def get():
    const = const_service.get_all()
    return jsonify({
        'response': {
            "appointments": models_to_json(const)
        }}), 200


# 修改参数
@const_app.route('/', methods=['POST'])
def modify():
    """
    eg = {
    "key": "a",
    "value": "b",
    }

    :return:
    :rtype:
    """
    return jsonify({
        'response': {
            "appointments": models_to_json(const)
        }}), 200
