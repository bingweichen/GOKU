# -*- coding: UTF-8 -*-
"""

@author: Bingwei Chen

@time: 8/4/17

@desc: storage route

1. storage Add/Get/Modify

"""
from flask import Blueprint
from flask import jsonify
from flask import request

from server.service import storage_service

PREFIX = '/storage'

storage_app = Blueprint("storage_app", __name__, url_prefix=PREFIX)


# ***************************** storage ***************************** #
# 通过 电动车型，颜色，数量添加
@storage_app.route('/', methods=['PUT'])  # test complete
def add_storage():
    """
    add storage

    eg = {
    "model": "E100小龟",
    "color": "红",
    "num": 50

    }

    :return:
    :rtype:
    """
    data = request.get_json()
    storage = storage_service.add(**data)
    if storage:
        return jsonify({'response': storage}), 200


# 通过型号，颜色获取库存
@storage_app.route('/', methods=['GET'])
def get_storage():
    model = request.args.get('model')
    color = request.args.get('color')

    if model is None:
        storage = storage_service.get_all()
    else:
        storage = [storage_service.get_by_model_color(model, color)]

    if storage:
        return jsonify({'response': {"storages": storage}}), 200
    else:
        return jsonify({'response': "no storage find"}), 404



# @storage_app.route('/<string:name>',
#                         methods=['POST'])  # test complete
# def modify_storage(name):
#     data = request.get_json()
#     modify_json = data
#     result = storage_service.modify_by_name(name, modify_json)
#     if result:
#         return jsonify({'response': "modify success"}), 200
#     else:
#         return jsonify({'response': "no storage find"}), 404
#     pass
#
#
# @storage_app.route('/<string:name>',
#                         methods=['DELETE'])  # test complete
# def remove_storage(name):
#     result = storage_service.remove_by_name(name)
#     if result:
#         return jsonify({'response': "delete success"}), 200
#     else:
#         return jsonify({'response': "no storage find"}), 404
#     pass

# ***************************** unit test ***************************** #

