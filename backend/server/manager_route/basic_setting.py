"""

@author: Bingwei Chen

@time: 8/4/17

@desc: 管理员

基础设置、

todo


取消订单设置、

账户注销设置、


"""

from flask import Blueprint
from flask import jsonify
from flask import request

from playhouse.shortcuts import model_to_dict

from server.service import e_bike_model_service
from server.service import storage_service
from server.service import const_service
from server.service import coupon_service

from server.utility.exception import Error
from server.utility.json_utility import models_to_json

PREFIX = '/manager/basic_setting'

basic_setting = Blueprint("basic_setting", __name__, url_prefix=PREFIX)


# 对电动车售卖价格设置、库存设置；电动车租赁价格设置、库存设置；

# ***************************** 电动车管理 ***************************** #
# 1. 获取所有电动车
@basic_setting.route('/e_bike_model/all', methods=['GET'])
def get_all_e_bike_models():
    e_bike_models = e_bike_model_service.get_all()
    return jsonify({
        'response': {
            "appointments": models_to_json(e_bike_models)
        }}), 200


# 2. 获取单个电动车
@basic_setting.route('/e_bike_model/<string:name>', methods=['GET'])
def get_e_bike_model(name):
    e_bike_model = e_bike_model_service.get_by_name(name)
    return jsonify({
        'response': {
            "e_bike_model": model_to_dict(e_bike_model),
        }
    }), 200


# 2. 更改电动车 (价格...)
@basic_setting.route('/e_bike_model/<string:name>', methods=['POST'])
def modify_e_bike_model(name):
    data = request.get_json()
    result = e_bike_model_service.modify_by_name(
        name,
        price=data.pop("price"),
        colors=data.pop("colors"),
        **data
    )
    return jsonify({'response': result}), 200
    pass


# ***************************** 库存管理 ***************************** #
# 1.获取库存
@basic_setting.route('/storage/all', methods=['GET'])
def get_all_storage():
    storage = storage_service.get_all()
    return jsonify({'response': models_to_json(storage)}), 200
    pass


# 2. 获取单个库存
@basic_setting.route('/storage', methods=['GET'])
def get_storage():
    model = request.args.get("model")
    color = request.args.get("color")
    storage = storage_service.get_by_model_color(model, color)
    return jsonify({'response': model_to_dict(storage)}), 200


# 3. 更改库存 (数量...)
@basic_setting.route('/storage/', methods=['POST'])
def modify_storage():
    data = request.get_json()
    result = storage_service.modify_num(
        model=data.pop("model"),
        color=data.pop("color"),
        num=data.pop("num"),
    )
    return jsonify({'response': result}), 200


# 对闪充价格设置
# 订单有效期时间设置、

# ***************************** 参数设置 ***************************** #
# 获取所有参数
@basic_setting.route('/', methods=['GET'])
def get():
    const = const_service.get_all()
    return jsonify({
        'response': {
            "appointments": models_to_json(const)
        }}), 200


# 修改参数
@basic_setting.route('/', methods=['POST'])
def modify():
    """
    eg = {
    "key": "a",
    "value": "b",
    }

    :return:
    :rtype:
    """
    data = request.get_json()
    result = const_service.modify(
        key=data.pop("key"),
        value=data.pop("value")
    )
    return jsonify({
        'response': {
            "result": result
        }}), 200


# 优惠券设置

# ***************************** 优惠券 ***************************** #
# 1. 添加优惠劵模板
@basic_setting.route('/coupon_template', methods=['PUT'])
def add_coupon_template():
    """
    eg = {
    "situation": 1000,
    "value": 100
    }

    :return:
    :rtype:
    """
    data = request.get_json()
    # situation = data.get("situation")
    # if situation:
    #     situation = data.pop("situation")
    coupon_template = coupon_service.add_coupon_template(
        situation=data.pop("situation"),
        value=data.pop("value"),
        **data
    )
    return jsonify({'response': coupon_template}), 200


# 2. 获取所有优惠劵模板
@basic_setting.route('/coupon_template/all', methods=['GET'])
def get_coupon_template():
    coupon_template = coupon_service.get_all_coupon_template()
    return jsonify({'response': coupon_template}), 200


# 3. 为所有用户添加优惠劵
@basic_setting.route('/coupon_to_all_user', methods=['PUT'])
def add_coupon_template_to_all_user():
    """
    eg = {
    "template_id": 1
    }

    :return:
    :rtype:
    """
    data = request.get_json()
    try:
        result = coupon_service.add_coupon_template_to_all_user(
            template_id=data.pop("template_id")
        )
        return jsonify({'response': result}), 200
    except Exception as e:
        return jsonify({'response': {
            "message": "错误",
            "error": e.args[1],
        }}), 400

