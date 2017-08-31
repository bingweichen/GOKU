# -*- coding: UTF-8 -*-
"""
@author: larry.shuoren@outlook.com
@author: bingweiChen

@time: 8/11/17
@desc: coupon route
"""
from flask import Blueprint
from flask import jsonify
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
# from playhouse.shortcuts import model_to_dict

from server.service import coupon_service
from server.utility.json_utility import models_to_json

PREFIX = '/coupon'

coupon = Blueprint("coupon", __name__, url_prefix=PREFIX)


# ***************************** 获取 ***************************** #
# 前端需更改
@coupon.route('', methods=['GET'])
@jwt_required
def get_my_coupons():
    """
    get all valid coupons of the user

    eg = coupon/bingwei

    :param user: user
    :return: valid coupons
    """
    username = get_jwt_identity()

    coup = coupon_service.get_my_coupons(
        user=username
    )
    return jsonify({'response': models_to_json(coup, recurse=False)}), 200
