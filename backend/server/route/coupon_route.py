# -*- coding: UTF-8 -*-
"""
@author: larry.shuoren@outlook.com
@time: 8/11/17
@desc: coupon route
"""

from flask import Blueprint
from flask import jsonify
from flask import request

from server.service import coupon_service

PREFIX = '/coupon'

coupon = Blueprint("coupon", __name__, url_prefix=PREFIX)


@coupon.route('/', methods=['POST'])
def add_coupon():
    """
    add a coupon to a user
    :return:
    """
    data = request.get_json()
    coup = coupon_service.add_coupon(**data)
    return jsonify({'response': coup}), 200


@coupon.route('/', methods=['POST'])
def use_coupon():
    """
    use coupon
    :return:
    """
    data = request.get_json()
    coup = coupon_service.use_coupon(data)
    return jsonify({'response': coup}), 200


@coupon.route('/<string:user>', methods=['GET'])
def get_my_coupons(user):
    """
    get all valid coupons of the user
    :param user: user
    :return: valid coupons
    """
    coup = coupon_service.get_my_coupons(user)
    return jsonify({'response': coup}), 200
