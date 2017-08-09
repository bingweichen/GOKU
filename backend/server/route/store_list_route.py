# -*- coding: UTF-8 -*-
"""

@author: Bingwei Chen

@time: 8/4/17

@desc: store_list route

1. store list Add/Get/Modify

"""
from flask import Blueprint
from flask import jsonify
from flask import request

from server.service import store_list_service

PREFIX = '/store_list'

store_list_app = Blueprint("store_list_app", __name__, url_prefix=PREFIX)


# ***************************** store_list ***************************** #
# 通过 电动车型，颜色，数量添加
@store_list_app.route('/', methods=['PUT'])  # test complete
def add_store_list():
    data = request.get_json()
    store_list = store_list_service.add(**data)
    if store_list:
        return jsonify({'response': store_list}), 200


# 通过型号，颜色获取库存
@store_list_app.route('/', methods=['GET'])
def get_store_list():
    model = request.args.get('model')
    color = request.args.get('color')

    if model is None:
        store_lists = store_list_service.get_all()
    else:
        store_lists = [store_list_service.get_by_model_color(model, color)]

    if store_lists:
        return jsonify({'response': {"store_lists": store_lists}}), 200
    else:
        return jsonify({'response': "no store_list find"}), 404


# @store_list_app.route('/<string:name>',
#                         methods=['POST'])  # test complete
# def modify_store_list(name):
#     data = request.get_json()
#     modify_json = data
#     result = store_list_service.modify_by_name(name, modify_json)
#     if result:
#         return jsonify({'response': "modify success"}), 200
#     else:
#         return jsonify({'response': "no store_list find"}), 404
#     pass
#
#
# @store_list_app.route('/<string:name>',
#                         methods=['DELETE'])  # test complete
# def remove_store_list(name):
#     result = store_list_service.remove_by_name(name)
#     if result:
#         return jsonify({'response': "delete success"}), 200
#     else:
#         return jsonify({'response': "no store_list find"}), 404
#     pass

# ***************************** unit test ***************************** #

