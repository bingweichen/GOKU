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
from flask_jwt_extended import jwt_required

from server.service import auth_decorator
from server.service import e_bike_model_service
from server.service import storage_service
from server.service import const_service
from server.service import coupon_service
from server.service import store_service
from server.service import school_service
from server.service import serial_number_service


from server.utility.json_utility import models_to_json
from server.utility.exception import Error

PREFIX = '/manager/basic_setting'

basic_setting = Blueprint("basic_setting", __name__, url_prefix=PREFIX)


# 对电动车售卖价格设置、库存设置；电动车租赁价格设置、库存设置；

# ***************************** 电动车管理 ***************************** #
# e_bike_model Add/Get/Modify/Remove
# 1. 获取所有电动车
@basic_setting.route('/e_bike_model/all', methods=['GET'])
@jwt_required
@auth_decorator.check_admin_auth
def get_all_e_bike_models():
    page = request.args.get("page")
    paginate_by = request.args.get("paginate_by")
    e_bike_models = e_bike_model_service.get_all(
        int(page),
        int(paginate_by)
    )
    total = e_bike_model_service.count_all()
    return jsonify({
        'response': {
            "total": total,
            "e_bike_models": models_to_json(e_bike_models, recurse=False)
        }}), 200


# 2. 获取单个电动车
@basic_setting.route('/e_bike_model/<string:name>', methods=['GET'])
@jwt_required
@auth_decorator.check_admin_auth
def get_e_bike_model(name):
    e_bike_model = e_bike_model_service.get_by_name(name)
    return jsonify({
        'response': {
            "e_bike_model": model_to_dict(e_bike_model, recurse=False),
        }
    }), 200


# 2. 更改电动车 (价格...)
@basic_setting.route('/e_bike_model', methods=['POST'])
@jwt_required
@auth_decorator.check_admin_auth
def modify_e_bike_model():
    """
    eg = {
     "name": "小龟电动车 爆款 48V、12A",
     "price": 1799,
     "colors": ["\u9ed1", "\u767d", "\u84dd", "\u7d2b", "\u8ff7\u5f69"]


"name": "小龟电动车 GB 48V、12A",
"price": 1980,
     "colors": [
                    "黑",
                    "白",
                    "蓝",
                    "紫",
                    "迷彩"
                ],
    }

    :param name:
    :type name:
    :return:
    :rtype:
    """
    data = request.get_json()
    # 转换价格
    _type = data["type"]
    price = data.pop("price")
    if _type == "租车":
        year_price = float(data.pop("year_price"))
        half_year_price = float(data.pop("half_year_price"))
        price = {
            "学期": half_year_price,
            "年": year_price
        }
    else:
        price = float(price)
    result = e_bike_model_service.modify_by_name(
        name=data.pop("name"),
        price=price,
        # colors=data.pop("colors"),
        **data
    )
    return jsonify({'response': result}), 200
    pass


# 添加车型
@basic_setting.route('/e_bike_model', methods=['PUT'])
@jwt_required
@auth_decorator.check_admin_auth
def add_e_bike_model():
    """
    eg = {
            "name": "小龟电动车 爆款 48V、12A1111",
            "colors": ["黑"、"白"、"蓝"、"紫"、"迷彩"],
            "configure": "低配",
            "battery": "48V、12A",
            "distance": "30KM",
            "price": "1699",
            "category": "小龟",
            "type": "买车"
        }

    :return:
    :rtype:
    """
    data = request.get_json()
    try:
        e_bike_model = e_bike_model_service.add(**data)
        e_bike_model = model_to_dict(e_bike_model, recurse=False)
        return jsonify({'response': e_bike_model}), 200
    except Error as e:
        return jsonify({'response': {
            "message": "错误",
            "error": e.args[1],
        }}), 400


# 删除车型
@basic_setting.route('/e_bike_model/<string:name>', methods=['DELETE'])
@jwt_required
@auth_decorator.check_admin_auth
def remove_e_bike_model(name):
    result = e_bike_model_service.remove_by_name(name)
    if result:
        return jsonify({'response': "delete success"}), 200
    else:
        return jsonify({'response': "no e_bike_model find"}), 404


# ***************************** 库存管理 ***************************** #
# 1.获取库存
@basic_setting.route('/storage/all', methods=['GET'])
@jwt_required
@auth_decorator.check_admin_auth
def get_all_storage():
    page = request.args.get("page")
    paginate_by = request.args.get("paginate_by")
    storage = storage_service.get_all_paginate(
        int(page),
        int(paginate_by)
    )
    total = storage_service.count_all()
    storage = models_to_json(storage, recurse=False)
    return jsonify({'response': {
        "total": total,
        "storage": storage
    }}), 200


# 2. 获取单个库存
@basic_setting.route('/storage', methods=['GET'])
@jwt_required
@auth_decorator.check_admin_auth
def get_storage():
    model = request.args.get("model")
    color = request.args.get("color")
    storage = storage_service.get_by_model_color(model, color)
    return jsonify({'response': model_to_dict(storage, recurse=False)}), 200


# 3. 更改库存 (数量...)
@basic_setting.route('/storage', methods=['POST'])
@jwt_required
@auth_decorator.check_admin_auth
def modify_storage():
    """
    eg = {
    "model": "小龟电动车 爆款 48V、12A",
    "color": "黑",
    "num": 100
    }
    :return:
    :rtype:
    """
    data = request.get_json()
    result = storage_service.modify_num(
        model=data.pop("model"),
        color=data.pop("color"),
        num=data.pop("num"),
    )
    return jsonify({'response': result}), 200


# 4.添加库存
@basic_setting.route('/storage', methods=['PUT'])
@jwt_required
@auth_decorator.check_admin_auth
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
    storage = storage_service.add(
        model=data.pop("model"),
        color=data.pop("color"),
        num=data.pop("num"),
    )
    if storage:
        return jsonify({'response': model_to_dict(storage, recurse=False)}), 200


# ***************************** 参数设置 ***************************** #
# 获取所有参数
@basic_setting.route('/const', methods=['GET'])
@jwt_required
@auth_decorator.check_admin_auth
def get():
    const = const_service.get_all()
    return jsonify({
        'response': {
            "const": models_to_json(const, recurse=False)
        }}), 200


# 修改参数
@basic_setting.route('/const', methods=['POST'])
@jwt_required
@auth_decorator.check_admin_auth
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
@jwt_required
@auth_decorator.check_admin_auth
def add_coupon_template():
    """
    eg = {
    "situation": 1000,
    "value": 100,

    "duration": 30,
    "desc": "满减"
    }

    :return:
    :rtype:
    """
    data = request.get_json()
    coupon_template = coupon_service.add_coupon_template(
        situation=data.pop("situation"),
        value=data.pop("value"),
        **data
    )
    coupon_template = model_to_dict(coupon_template, recurse=False)
    return jsonify({'response': coupon_template}), 200


# 2. 获取所有优惠劵模板
@basic_setting.route('/coupon_template/all', methods=['GET'])
@jwt_required
@auth_decorator.check_admin_auth
def get_coupon_template():
    coupon_template = coupon_service.get_all_coupon_template()
    coupon_template = models_to_json(coupon_template, recurse=False)
    return jsonify({'response': coupon_template}), 200


# 获取所有用户的优惠劵
@basic_setting.route('/coupon/all', methods=['GET'])
@jwt_required
@auth_decorator.check_admin_auth
def get_coupon():
    coupon = coupon_service.get_all_coupon()
    coupon = models_to_json(coupon, recurse=False)
    return jsonify({'response': coupon}), 200


# 3. 为所有用户添加优惠劵
@basic_setting.route('/coupon_to_all_user', methods=['PUT'])
@jwt_required
@auth_decorator.check_admin_auth
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
        return jsonify({'response': {
            "result": result,
            "message": "添加优惠劵成功"
        }}), 200
    except Error as e:
        return jsonify({'response': {
            "message": "错误",
            "error": e.args[1],
        }}), 400


# ***************************** 商铺管理 ***************************** #
@basic_setting.route('/store', methods=['PUT'])
@jwt_required
@auth_decorator.check_admin_auth
def add_store():
    data = request.get_json()
    store = store_service.add(**data)
    if store:
        store = model_to_dict(store, recurse=False)
        return jsonify({'response': store}), 200
    pass


@basic_setting.route('/store/all', methods=['GET'])
@jwt_required
@auth_decorator.check_admin_auth
def get_stores():
    """

    :return:
    :rtype:
    """
    stores = store_service.get_all()
    return jsonify({
        'response': {
            "stores": models_to_json(stores, recurse=False),
        }}), 200


@basic_setting.route('/store', methods=['POST'])
@jwt_required
@auth_decorator.check_admin_auth
def modify_store():
    """

    :return:
    :rtype:
    """
    data = request.get_json()
    result = store_service.modify_by_name(
        name=data.pop('name'),
        modify_json=data
    )
    if result:
        return jsonify({'response': "modify success"}), 200
    else:
        return jsonify({'response': "no store find"}), 404
    pass


@basic_setting.route('/store/<string:name>', methods=['DELETE'])
@jwt_required
@auth_decorator.check_admin_auth
def remove_store(name):
    result = store_service.remove_by_name(name)
    if result:
        return jsonify({'response': "delete success"}), 200
    else:
        return jsonify({'response': "no store find"}), 404


# ***************************** 学校管理 ***************************** #
@basic_setting.route('/school/all', methods=['GET'])
@jwt_required
@auth_decorator.check_admin_auth
def get_schools():
    """

    :return:
    :rtype:
    """
    school = school_service.get_all()
    return jsonify({
        'response': {
            "schools": models_to_json(school, recurse=False),
        }}), 200

@basic_setting.route('/school', methods=['PUT'])
@jwt_required
@auth_decorator.check_admin_auth
def add_school():
    data = request.get_json()
    school = school_service.add(**data)
    if school:
        school = model_to_dict(school, recurse=False)
        return jsonify({'response': school}), 200


@basic_setting.route('/school', methods=['POST'])
@jwt_required
@auth_decorator.check_admin_auth
def modify_school():
    data = request.get_json()
    result = school_service.modify_by_name(
        name=data.pop('name'),
        modify_json=data
    )
    if result:
        return jsonify({'response': "modify success"}), 200
    else:
        return jsonify({'response': "no school find"}), 404
    pass


@basic_setting.route('/school/<string:name>', methods=['DELETE'])
@jwt_required
@auth_decorator.check_admin_auth
def remove_school(name):
    result = school_service.remove_by_name(name)
    if result:
        return jsonify({'response': "delete success"}), 200
    else:
        return jsonify({'response': "no school find"}), 404
    pass


# ***************************** 编号管理 ***************************** #
@basic_setting.route('/serial_number/all', methods=['GET'])
@jwt_required
@auth_decorator.check_admin_auth
def get_all_serial_number():
    serial_number, total = serial_number_service.get_all(
        page=int(request.args.get("page")),
        paginate_by=int(request.args.get("paginate_by"))
    )
    return jsonify({'response': {
        "serial_number": models_to_json(serial_number, recurse=False),
        "total": total
    }}), 200



# 暂时没用
# @coupon.route('', methods=['PUT'])
# def add_coupon():
#     """
#     add a coupon to a user
#
#     eg = {
#      "user": "bingwei",
#      "situation": 1000,
#      "value": 100,
#      "expired" : "20170910"
#     }
#     :return:
#     """
#     data = request.get_json()
#     expired = data.pop("expired")
#     coup = coupon_service.add_coupon(
#         expired=expired, **data
#     )
#     return jsonify({'response': coup}), 200
