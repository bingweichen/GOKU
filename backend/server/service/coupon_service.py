# -*- coding: UTF-8 -*-
"""
@author: larry.shuoren@outlook.com
@author: bingweiChen

@time: 8/11/17
@desc: coupon service
"""

from datetime import datetime, timedelta

from server.database.model import Coupon, CouponTemplate, User
# from server.utility.json_utility import models_to_json, model_to_dict
from server.utility.exception import *


def get_all_coupon_template():
    coupon_template = CouponTemplate.select()
    return coupon_template


def add_coupon(**kwargs):
    """
    add a coupon to a user
    :param kwargs: coupon information
    :return:
    """
    desc = ""
    if "situation" in kwargs and "value" in kwargs:
        desc = "满%s减%s" % (kwargs["situation"], kwargs["value"])
    if "duration" not in kwargs:
        kwargs.update({"duration": 3650})
    coupon = Coupon.create(desc=desc or "通用", **kwargs)
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
    coupon = Coupon.get(Coupon.id == c_id)
    if user != coupon.user.username:
        raise Error("User not matched")
    if coupon.status != "可用":
        raise Error("This coupon cannot be used any more")
    if coupon.situation > before_price:
        raise Error("situation not suitable")
    coupon.status = "已使用"
    after_price = before_price - coupon.value
    coupon.save()
    return after_price


def add_coupon_template_to_all_user(template_id):
    template = CouponTemplate.get(CouponTemplate.id == template_id)
    today = datetime.today().replace(hour=0, minute=0,
                                     second=0, microsecond=0)
    expired = today + timedelta(days=template.duration)
    data = {"desc": template.desc, "situation": template.situation,
            "value": template.value, "expired": expired,
            "template_no": template_id}
    users = User.select(User.username)
    for u in users:
        Coupon.create(user=u.username, **data)
    return True


def add_coupon_template(**kwargs):
    desc = ""
    if "situation" in kwargs and "value" in kwargs:
        desc = "满%s减%s" % (kwargs["situation"], kwargs["value"])
    if "duration" not in kwargs:
        kwargs.update({"duration": 3650})
    c_t = CouponTemplate.create(desc=desc or "通用", **kwargs)
    return c_t


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
    # add_template()
    # add_coupon_template(value=100)
    # add_coupon_template_to_all_user(1)
    pass
