# -*- coding: UTF-8 -*-

"""

@author: Bingwei Chen

@time: 2017.08.07

@desc: service for e_bike_model

1. e_bike_model Add/Get/Modify/Remove

"""

# from playhouse.shortcuts import model_to_dict

from server.database.model import EBikeModel
from server.utility.json_utility import models_to_json
from server.utility.service_utility import *


def add(**kwargs):
    """
    add e_bike_model

    eg = {
    "name": "E100小龟",
    "category": "小龟",
    "price": 2000,
    "colors": "红，蓝，绿",
    "introduction": "小龟电动车",
    }

    :param kwargs:
    :type kwargs:
    :return: the added json
    :rtype: json
    """
    e_bike_model = EBikeModel.create(**kwargs)
    return e_bike_model


def get(*query, **kwargs):
    e_bike_model = EBikeModel.get(*query, **kwargs)
    return e_bike_model


def get_all(page, paginate_by):
    e_bike_models = EBikeModel.select().paginate(page, paginate_by)
    return e_bike_models


def get_all_paginate():
    e_bike_models = EBikeModel.select()
    return e_bike_models


def count_all():
    count = EBikeModel.select().count()
    return count

def get_by_name(name):
    return EBikeModel.get(EBikeModel.name == name)


def get_by_category(category):
    e_bike_models = EBikeModel.select().where(EBikeModel.category == category)
    return e_bike_models


def modify_by_name(name, **modify_json):
    """

    :param name:
    :type name:
    :param modify_json:
    :type modify_json:
    :return: number of row update, 0 if not find, error if modify_json is wrong
    :rtype: int
    """
    query = EBikeModel.update(**modify_json).where(EBikeModel.name == name)
    return query.execute()


def num_view_increment(name):
    # 获取num_view
    # 递增num_view
    query = EBikeModel.update(num_view=EBikeModel.num_view + 1) \
        .where(EBikeModel.name == name)
    return query.execute()


def remove_by_name(name):
    query = EBikeModel.delete().where(EBikeModel.name == name)
    return query.execute()


# ***************************** unit test ***************************** #
def add_template():
    template_json = [
        # 小龟
        {
            "name": "小龟电动车 爆款 48V、12A",
            "colors": "黑、白、蓝、紫、迷彩",
            "configure": "低配",
            "battery": "48V、12A",
            "distance": "30KM",
            "price": "1699RMB",
            "category": "小龟",
        },
        {
            "name": "小龟电动车 GB 48V、12A",
            "colors": "黑、白、蓝、紫、迷彩",
            "configure": "中高配",
            "battery": "48V、12A",
            "distance": "30KM",
            "price": "1980RMB",
            "category": "小龟"
        },
        {
            "name": "小龟电动车 GC 48V、12A",
            "colors": "黑、白、蓝、紫、迷彩",
            "configure": "高配",
            "battery": "48V、12A",
            "distance": "30KM",
            "price": "2080RMB",
            "category": "小龟"
        },
        {
            "name": "小龟电动车 OA 48V、20A",
            "colors": "黑、白、蓝、紫、迷彩",
            "configure": "低配",
            "battery": "48V、20A   ",
            "distance": "40~45KM",
            "price": "2080RMB",
            "category": "小龟"
        },
        {
            "name": "小龟电动车 OB 48V、20A",
            "colors": "黑、白、蓝、紫、迷彩",
            "configure": "中高配",
            "battery": "48V、20A     ",
            "distance": "40~45KM",
            "price": "2180RMB",
            "category": "小龟"
        },
        {
            "name": "小龟电动车 OC 48V、20A",
            "colors": "黑、白、蓝、紫、迷彩",
            "configure": "高配",
            "battery": "48V、20A     ",
            "distance": "40~45KM",
            "price": "2280RMB",
            "category": "小龟"
        },
        {
            "name": "小龟电动车 KA 60V、12A",
            "colors": "黑、白、蓝、紫、迷彩",
            "configure": "低配",
            "battery": "60V、12A  ",
            "distance": "30KM",
            "price": "1980RMB",
            "category": "小龟"
        },
        {
            "name": "小龟电动车 KB 60V、12A",
            "colors": "黑、白、蓝、紫、迷彩",
            "configure": "中高配",
            "battery": "60V、12A     ",
            "distance": "30KM",
            "price": "2080RMB",
            "category": "小龟"
        },
        {
            "name": "小龟电动车 KC 60V、12A",
            "colors": "黑、白、蓝、紫、迷彩",
            "configure": "高配",
            "battery": "60V、12A     ",
            "distance": "30KM",
            "price": "2180RMB",
            "category": "小龟"
        },
        {
            "name": "小龟电动车 GA 60V、20A",
            "colors": "黑、白、蓝、紫、迷彩",
            "configure": "低配",
            "battery": "60V、20A",
            "distance": "55~60KM",
            "price": "2280RMB",
            "category": "小龟"
        },
        {
            "name": "小龟电动车 GB 60V、20A",
            "colors": "黑、白、蓝、紫、迷彩",
            "configure": "中高配",
            "battery": "60V、20A",
            "distance": "55~60KM",
            "price": "2380RMB",
            "category": "小龟"
        },
        {
            "name": "小龟电动车 GC 60V、20A",
            "colors": "黑、白、蓝、紫、迷彩",
            "configure": "高配",
            "battery": "60V、20A",
            "distance": "55~60KM",
            "price": "2480RMB",
            "category": "小龟"
        },
        {
            "name": "小龟电动车 PA 72V、20A",
            "colors": "黑、白、蓝、紫、迷彩",
            "configure": "低配",
            "battery": "72V、20A   ",
            "distance": "60~70KM",
            "price": "2480RMB",
            "category": "小龟"
        },
        {
            "name": "小龟电动车 PB 72V、20A",
            "colors": "黑、白、蓝、紫、迷彩",
            "configure": "中高配",
            "battery": "72V、20A     ",
            "distance": "60~70KM",
            "price": "2580RMB",
            "category": "小龟"
        },
        {
            "name": "小龟电动车 PC 72V、20A",
            "colors": "黑、白、蓝、紫、迷彩",
            "configure": "高配",
            "battery": "72V、20A     ",
            "distance": "60~70KM",
            "price": "2680RMB",
            "category": "小龟"
        },

        # 酷车
        {
            "name": "酷车 小猴子 72V、20A",
            "category": "酷车",
            "price": "4200RMB",
            "distance": "60KM以上",
            "colors": "磨砂、镀金",
            "configure": "配置任选",
            "battery": "72V、20A"
        },
        {
            "name": "酷车 地平线 72V、20A",
            "category": "酷车",
            "price": "4200RMB",
            "distance": "60KM以上",
            "colors": "炫红、酷蓝",
            "configure": "跑车配置",
            "battery": "72V、20A"
        },
        {
            "name": "酷车 小怪兽 72V、20A",
            "category": "酷车",
            "price": "4200RMB",
            "distance": "60KM以上",
            "colors": "拼色、酷黑",
            "configure": "配置任选",
            "battery": "72V、20A"
        },
        {
            "name": "酷车 祖马 72V、20A",
            "category": "酷车",
            "price": "3200RMB",
            "distance": "60KM以上",
            "colors": "黑",
            "configure": "配置任选",
            "battery": "72V、20A"
        },
        {
            "name": "酷车 路虎 72V、20A",
            "category": "酷车",
            "price": "4000RMB",
            "distance": "60KM以上",
            "colors": "任选",
            "configure": "配置任选",
            "battery": "72V、20A"
        },

        # 租车
        {
            "name": "闪租 48V、20A",
            "category": "闪租",
            "price": "588/学期；998/年",
            "distance": "40~45KM",
            "colors": "黑、白、银、迷彩",
            "configure": "高配",
            "battery": "48V、20A"
        },
        {
            "name": "闪租 60V、20A",
            "category": "闪租",
            "price": "588/学期；999/年",
            "distance": "55~60KM",
            "colors": "黑、白、银、迷彩",
            "configure": "高配",
            "battery": "60V、20A"
        },
        {
            "name": "MINI 48V、20A",
            "category": "MINI租",
            "price": "298/学期；588/年",
            "distance": "35KM",
            "colors": "红、紫、蓝、白",
            "configure": "高配",
            "battery": "48V、20A"
        },
    ]

    category_type = {
        "酷车": "买车",
        "小龟": "买车",
        "闪租": "租车",
        "MINI租": "租车"
    }
    # add url to json
    url = "http://ouhx8b81v.bkt.clouddn.com/"
    for i in range(len(template_json)):
        # 将 colors 转成数组
        colors = template_json[i]["colors"]
        colors = colors.split("、")
        template_json[i]["colors"] = colors
        # 存入type
        template_json[i]["type"] = category_type[template_json[i]["category"]]
        # 将 image_urls 存入
        image_url = "%s%s.png_1" % (url, template_json[i]["name"])
        template_json[i]["image_urls"] = [image_url]
        introduction_image_url = \
            "%s%s.png_intro_1" % (url, template_json[i]["name"])
        template_json[i]["introduction_image_urls"] = [introduction_image_url]

        # price
        price = template_json[i]["price"]
        if template_json[i]["type"] == "租车":
            prices = price.split("；")
            price = {
                "学期": float(filter_number(prices[0])),
                "年": float(filter_number(prices[1]))
            }
        else:
            price = float(filter_number(price))
        template_json[i]["price"] = price

    for json in template_json:
        result = add(**json)
        print(result)


if __name__ == '__main__':
    pass
    print(add_template())
