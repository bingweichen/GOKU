# -*- coding: UTF-8 -*-
"""

@author: Bingwei Chen

@time: 8/4/17

@desc: e_bike_model route

1. e_bike_model Add/Get/Modify/Remove

1. 电动车类型列表
localhost:5000/e_bike_model?category=小龟
localhost:5000/e_bike_model?category=酷车
localhost:5000/e_bike_model?category=租车
2. 单个电动车类型详情
localhost:5000/e_bike_model/<string:name>
localhost:5000/e_bike_model/小龟电动车 爆款 48V、12A

"""
from flask import Blueprint
from flask import jsonify
from flask import request

from playhouse.shortcuts import model_to_dict


from server.service import e_bike_model_service
from server.utility.logger import logger
from server.utility.json_utility import models_to_json

PREFIX = '/e_bike_model'

e_bike_model_app = Blueprint("e_bike_model_app", __name__, url_prefix=PREFIX)


# 1. 电动车类型列表
@e_bike_model_app.route('/', methods=['GET'])
def get_e_bike_model():
    category = request.args.get('category')
    if category is None:
        e_bike_models = e_bike_model_service.get_all()
    else:
        e_bike_models = e_bike_model_service.get_by_category(category)

    if e_bike_models:
        return jsonify({
            'response': {
                "e_bike_models": models_to_json(e_bike_models)
            }}), 200
    else:
        return jsonify({'response': "no e_bike_model find"}), 404


# 2. 单个电动车类型详情
@e_bike_model_app.route('/<string:name>', methods=['GET'])
def get_e_bike_model_one(name):
    """
    # 单独获取一个
    # 当调用这个api时该车型浏览量加一
    :param name:
    :type name:
    :return:
    :rtype:
    """
    e_bike_model = e_bike_model_service.get_by_name(name)
    if e_bike_model:
        # 递增
        result = e_bike_model_service.num_view_increment(name)
        logger.debug("increment", result)

        return jsonify({
            'response':
                {"e_bike_model": model_to_dict(e_bike_model)}}), 200
    else:
        return jsonify({'response': "no e_bike_model find"}), 404


@e_bike_model_app.route('/', methods=['PUT'])  # test complete
def add_e_bike_model():
    data = request.get_json()
    e_bike_model = e_bike_model_service.add(**data)
    if e_bike_model:
        return jsonify({'response': e_bike_model}), 200
    pass


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
