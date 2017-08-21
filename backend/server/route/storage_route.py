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
# from playhouse.shortcuts import model_to_dict
from server.utility.json_utility import models_to_json

PREFIX = '/storage'

storage_app = Blueprint("storage_app", __name__, url_prefix=PREFIX)


# ***************************** storage ***************************** #
# 通过型号，颜色获取库存
@storage_app.route('', methods=['GET'])
def get_storage():
    model = request.args.get('model')
    color = request.args.get('color')

    if model is None:
        storage = storage_service.get_all()
    else:
        storage = [storage_service.get_by_model_color(model, color)]

    if storage:
        return jsonify({'response': {"storages": models_to_json(storage)}}), 200
    else:
        return jsonify({'response': "no storage find"}), 404

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
