# -*- coding: UTF-8 -*-

"""
@author: Shuo Ren
@time: 8/9/17
@desc: e-bike rent service
"""

from playhouse.shortcuts import model_to_dict

from server.database.model import EBike
# from server.utility.json_utility import models_to_json


def add(**kwargs):
    """

    :param kwargs:
    :type kwargs:
    :return: the added json
    :rtype: json
    """
    e_bike = EBike.create(**kwargs)
    return model_to_dict(e_bike)


def modify_user(plate_no, user):
    if not user:
        status = "空闲"
    else:
        status = "已租"
    statement = EBike.update(user=user, status=status).where(EBike.plate_no == plate_no)
    return statement.execute()


def get_available_e_bike_models():
    e_bikes = EBike.select(EBike.model, EBike.color).distinct().where(EBike.status == "空闲")
    query = e_bikes.execute()
    result = []
    for i in query:
        result.append({"model_name": model_to_dict(i.model)["name"], "color": i.color})
    return result


def get_e_bike_model_information(name):
    info = EBike.get(name=name)
    return model_to_dict(info)


# ----------------for test----------------
def add_template():
    template_json = [
        {
            "plate_no": "001",
            "model": "E100小龟",
            "color": "红",
        },
        {
            "plate_no": "002",
            "model": "E100小龟",
            "color": "黄",
        },
        {
            "plate_no": "003",
            "model": "E100小龟",
            "color": "绿",
        }
    ]
    for json in template_json:
        result = add(**json)
        print(result)


if __name__ == '__main__':
    # add_template()
    # modify_user("001", "hahaha")
    print(get_available_e_bike_models())
