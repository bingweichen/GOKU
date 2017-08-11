# -*- coding: UTF-8 -*-
"""
@author: larry.shuoren@outlook.com
@time: 8/11/17
@desc: coupon service
"""

from datetime import datetime
from playhouse.shortcuts import model_to_dict

from server.database.model import Coupon
from server.utility.json_utility import models_to_json


def add_coupon(**kwargs):
    """
    add a coupon to a user
    :param kwargs: coupon information
    :return:
    """
    coupon = Coupon.create(**kwargs)
    return model_to_dict(coupon)


def use_coupon(data):
    """
    use a coupon
    :param data: coupon information
    :return: 
    """
    user = data["user"]
    c_id = data["c_id"]
    coupon_info = Coupon.get(Coupon.user == user)
    if user != models_to_json(coupon_info)["user"]:
        return "User not matched"
    if coupon_info["status"] != "可用":
        return "This coupon cannot be used any more"
    coupon = Coupon.update(status="已使用").where(Coupon.id == c_id)
    coupon.execute()
    return "Coupon used succeed"


def get_my_coupons(user):
    """
    get valid coupons
    :param user: user of coupon
    :return: valid coupons
    """
    now = datetime.now()
    coupon = Coupon.update(status="过期").where(
        Coupon.user == user, Coupon.status == "可用", Coupon.expired < now)
    coupon.execute()
    coupon = Coupon.select().where(Coupon.user == user, Coupon.status == "可用")
    coupon = models_to_json(coupon)
    return coupon

