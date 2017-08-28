# -*- coding: UTF-8 -*-
"""
@author: larry.shuoren@outlook.com
@author: bingweiChen

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


# ***************************** 获取 ***************************** #
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
    return jsonify({'response': models_to_json(coup, recurse=False)}), 200

