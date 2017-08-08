# -*- coding: UTF-8 -*-
"""

@author: Bingwei Chen

@time: 8/4/17

@desc: resource route

1. e_bike_model Add/Get/Modify/Remove

"""
from flask import Blueprint
from flask import jsonify
from flask import request

from server.service import e_bike_model_service

PREFIX = '/e_bike_model'

e_bike_model_app = Blueprint("e_bike_model_app", __name__, url_prefix=PREFIX)


# ***************************** e_bike_model ***************************** #
@e_bike_model_app.route('/', methods=['PUT'])  # test complete
def add_e_bike_model():
    data = request.get_json()
    e_bike_model = e_bike_model_service.add(**data)
    if e_bike_model:
        return jsonify({'response': e_bike_model}), 200
    pass


# # 单独获取一个
# @e_bike_model_app.route('/<string:name>', methods=['GET'])
# def get_e_bike_model_one(name):
#     e_bike_model = e_bike_model_service.get_by_name(name)
#     if e_bike_model:
#         return jsonify({'response': {"e_bike_model": e_bike_model}}), 200
#     else:
#         return jsonify({'response': "no e_bike_model find"}), 404


@e_bike_model_app.route('/', methods=['GET'])
def get_e_bike_model():
    category = request.args.get('category')
    if category is None:
        e_bike_models = e_bike_model_service.get_all()
    else:
        e_bike_models = [e_bike_model_service.get_by_category(category)]

    if e_bike_models:
        return jsonify({'response': {"e_bike_models": e_bike_models}}), 200
    else:
        return jsonify({'response': "no e_bike_model find"}), 404


@e_bike_model_app.route('/<string:name>',
                        methods=['POST'])  # test complete
def modify_e_bike_model(name):
    data = request.get_json()
    modify_json = data
    result = e_bike_model_service.modify_by_name(name, modify_json)
    if result:
        return jsonify({'response': "modify success"}), 200
    else:
        return jsonify({'response': "no e_bike_model find"}), 404
    pass


@e_bike_model_app.route('/<string:name>',
                        methods=['DELETE'])  # test complete
def remove_e_bike_model(name):
    result = e_bike_model_service.remove_by_name(name)
    if result:
        return jsonify({'response': "delete success"}), 200
    else:
        return jsonify({'response': "no e_bike_model find"}), 404
    pass

# ***************************** unit test ***************************** #
# 获取小龟列表
# localhost:5000/e_bike_model?category=小龟
# 获取酷车列表
# localhost:5000/e_bike_model?category=酷车
# 获取闪租列表
# localhost:5000/e_bike_model?category=闪租
# 获取迷你租列表
# localhost:5000/e_bike_model?category=迷你租
