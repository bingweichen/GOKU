"""

@author: Bingwei Chen

@time: 8/4/17

@desc: 管理员

电动车售卖价格设置
"""

from flask import Blueprint
from flask import jsonify
from flask import request

from playhouse.shortcuts import model_to_dict

from server.service import appointment_service
from server.service import user_service
from server.service import e_bike_model_service
from server.service import storage_service
# from server.service import appointment_service


from server.utility.exception import Error
from server.utility.json_utility import models_to_json

PREFIX = '/manager'

manager = Blueprint("manager", __name__, url_prefix=PREFIX)


# 获取所有订单
@manager.route('/appointments', methods=['GET'])
def get_appointments():
    appointments = appointment_service.get_all()
    return jsonify({
        'response': {
            "appointments": models_to_json(appointments)
        }}), 200


# 获取订单
@manager.route('/appointment/<string:appointment_id>', methods=['GET'])
def get_appointment(appointment_id=None):
    appointment = appointment_service.get_by_id(appointment_id)
    return jsonify({
        'response': {
            "appointment": model_to_dict(appointment)}}), 200


# 取消订单设置
@manager.route('/appointment/status/cancel',
               methods=['POST'])
def cancel_appointment():
    """
    appointment_id: int

    eg = {
    "appointment_id": 3,
    }
    :return: 1 for success
    :rtype:
    """
    data = request.get_json()
    appointment_id = data["appointment_id"]
    result = appointment_service.cancel_appointment(appointment_id)
    if result:
        return jsonify({'response': result}), 200
    pass


# 电动车售卖价格设置
# 1.获取所有电动车
@manager.route('/e_bike_model/all', methods=['GET'])
def get_all_e_bike_models():
    e_bike_models = e_bike_model_service.get_all()
    return jsonify({
        'response': {
            "appointments": models_to_json(e_bike_models)
        }}), 200


# 2. 获取单个电动车
@manager.route('/e_bike_model/<string:name>', methods=['GET'])
def get_e_bike_model(name):
    e_bike_model = e_bike_model_service.get_by_name(name)
    return jsonify({
        'response': {
            "e_bike_model": model_to_dict(e_bike_model),
        }
    }), 200


# 3. 更改电动车 (价格...)
@manager.route('/e_bike_model/<string:name>', methods=['POST'])
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


# 库存设置
# 1.获取库存
@manager.route('/storage/all', methods=['GET'])
def get_all_storage():
    storage = storage_service.get_all()
    return jsonify({'response': models_to_json(storage)}), 200
    pass


# 2. 获取单个库存
@manager.route('/storage', methods=['GET'])
def get_storage():
    model = request.args.get("model")
    color = request.args.get("color")
    storage = storage_service.get_by_model_color(model, color)
    return jsonify({'response': model_to_dict(storage)}), 200


# 3. 更改库存 (数量...)
@manager.route('/storage/', methods=['POST'])
def modify_storage():
    data = request.get_json()
    result = storage_service.modify_num(
        model=data.pop("model"),
        color=data.pop("color"),
        num=data.pop("num"),
    )
    return jsonify({'response': result}), 200


# 闪充价格设置（暂时忽略）
# 最晚归还时间设置和两周后每超过一天进行扣费设置，最晚一个月未归还直接冻结
# 个人账户、押金金额、冻结账户设置（暂时忽略）


# 优惠券设置
# 查看优惠劵类型

# 为所有用户添加优惠劵 某类优惠劵
@manager.route('/coupon/', methods=['POST'])
def add_coupon_to_users():
    data = request.get_json()
    coupon_template_id = data["coupon_template_id"]
    pass


# 用户查看
@manager.route('/users/', methods=['GET'])
def get_all_users():
    users = user_service.get_all()
    users = models_to_json(users)
    for i in range(len(users)):
        users[i].pop("password")
    return jsonify({'response': users}), 200
    pass
