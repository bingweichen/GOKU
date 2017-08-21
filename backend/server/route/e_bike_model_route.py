# -*- coding: UTF-8 -*-
"""

@author: Bingwei Chen

@time: 8/4/17

@desc: e_bike_model route

1. e_bike_model /Get/

1. 电动车类型列表
localhost:5000/e_bike_model?category=小龟
2. 单个电动车类型详情
localhost:5000/e_bike_model/<string:name>   eg=小龟电动车 爆款 48V、12A
"""
from flask import Blueprint
from flask import jsonify
from flask import request

from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist

from server.service import e_bike_model_service
from server.utility.logger import logger
from server.utility.json_utility import models_to_json
from server.utility.constant.custom_constant import get_custom_const

PREFIX = '/e_bike_model'

e_bike_model_app = Blueprint("e_bike_model_app", __name__, url_prefix=PREFIX)


# ***************************** 查询 ***************************** #
# 1. 电动车类型列表
@e_bike_model_app.route('', methods=['GET'])
def get_e_bike_model():
    category = request.args.get('category')
    # if category is None:
    #     e_bike_models = e_bike_model_service.get_all()
    # else:
    e_bike_models = e_bike_model_service.get_by_category(category)
    return jsonify({
        'response': {
            "e_bike_models": models_to_json(e_bike_models)
        }}), 200


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

    try:
        e_bike_model = e_bike_model_service.get_by_name(name)
        result = e_bike_model_service.num_view_increment(name)
        logger.info("increment", result)

        return jsonify({
            'response': {
                "e_bike_model": model_to_dict(e_bike_model),
                "appointment_fee":
                    get_custom_const("DEFAULT_APPOINTMENT_FEE")
            }
        }), 200
    except DoesNotExist as e:
        return jsonify({
            'response': {
                "error": '%s: %s' % (str(DoesNotExist), e.args),
                "message": "无该车型"
            }}), 404

# ***************************** unit test ***************************** #
