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
from server.utility.exception import *


def add_coupon(**kwargs):
    """
    add a coupon to a user
    :param kwargs: coupon information
    :return:
    """
    coupon = Coupon.create(**kwargs)
    return coupon


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
    coupon = Coupon.select().where(
        Coupon.user == user, Coupon.status == "可用")
    return coupon


def use_coupon(user, c_id, before_price):
    """
    check if coupon belonging to the user
    use coupon and get price after using coupon
    change the status of coupon into invalid
    :param user: username
    :param c_id: coupon id
    :param before_price: price before using coupon
    :return: price after using coupon
    """
    coupon_info = Coupon.get(Coupon.user == user)
    if user != models_to_json(coupon_info)["user"]:
        raise Error("User not matched")
    if coupon_info["status"] != "可用":
        raise Error("This coupon cannot be used any more")
    coupon = Coupon.update(status="已使用").where(Coupon.id == c_id)
    coupon.execute()
    after_price = Coupon.select().where(coupon.id == c_id)
    after_price = before_price - models_to_json(after_price)["value"]
    return after_price


# ***************************** unit test ***************************** #
def add_template():
    template_json = [
        {
            "user": "bingwei",
            "situation": 1000,
            "value": 100,
            "expired": "20170910",
            "desc": "满1000减100"
        }
    ]
    for json in template_json:
        result = add_coupon(**json)
        print(result)

if __name__ == "__main__":
    add_template()