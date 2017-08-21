# -*- coding: UTF-8 -*-
"""
@author: larry.shuoren@outlook.com
@time: 8/11/17
@desc: coupon route
"""
from datetime import datetime, timedelta
from flask import Blueprint
from flask import jsonify
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from playhouse.shortcuts import model_to_dict

from server.service import coupon_service
from server.service import auth_decorator
from server.utility.json_utility import models_to_json
PREFIX = '/coupon'

coupon = Blueprint("coupon", __name__, url_prefix=PREFIX)


@coupon.route('', methods=['PUT'])
def add_coupon():
    """
    add a coupon to a user

    eg = {
     "user": "bingwei",
     "situation": 1000,
     "value": 100,
     "expired" : "20170910"
    }
    :return:
    """
    data = request.get_json()
    expired = data.pop("expired")
    coup = coupon_service.add_coupon(
        expired=expired, **data
    )
    return jsonify({'response': coup}), 200


@coupon.route('/<string:user>', methods=['GET'])
# @jwt_required
# @auth_decorator.requires_auth
def get_my_coupons(user):
    """
    get all valid coupons of the user

    eg = coupon/bingwei

    :param user: user
    :return: valid coupons
    """
    # current_user = get_jwt_identity()
    # print("current_user", current_user)

    coup = coupon_service.get_my_coupons(user)
    return jsonify({'response': models_to_json(coup)}), 200

# @coupon.route('/', methods=['POST'])
# def use_coupon():
#     """
#     use coupon
#     :return:
#     """
#     data = request.get_json()
#     coup = coupon_service.use_coupon(data)
#     return jsonify({'response': coup}), 200


@coupon.route('/coupon_template', methods=['POST'])
def add_coupon_template_to_all_user():
    data = request.get_json()
    template_id = data.pop("template_id")
    coupon_service.add_coupon_template_to_all_user(template_id)


@coupon.route('/coupon_template', methods=['POST'])
def add_coupon_template():
    data = request.get_json()
    coupon_template = coupon_service.add_coupon_template(**data)
    return jsonify({'response': coupon_template}), 200
