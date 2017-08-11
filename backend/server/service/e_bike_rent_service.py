# -*- coding: UTF-8 -*-

"""
@author: larry.shuoren@outlook.com
@time: 8/9/17
@desc: e-bike rent service
"""

from playhouse.shortcuts import model_to_dict

from server.database.model import EBike
from server.database.model import EBikeModel
# from server.utility.json_utility import models_to_json


def add(**kwargs):
    """
    add new virtual card
    :param kwargs: parameters to insert in database
    :return:
    """
    e_bike = EBike.create(**kwargs)
    return model_to_dict(e_bike)


def modify_user(data):
    """
    modify the user of e-bike
    :param data:
        plate_no: plate number of e-bike
        user: user of e-bike
    :return:
    """
    user = data["user"]
    plate_no = data["plate_no"]
    if not user:
        status = "空闲"
    else:
        status = "已租"
    statement = EBike.update(user=user, status=status
                             ).where(EBike.plate_no == plate_no)
    return statement.execute()


def get_available_e_bike_models():
    """
    get available e-bike models
    :return: available e-bike models
    """
    e_bikes = EBike.select(EBike.model, EBike.color
                           ).distinct().where(EBike.status == "空闲")
    query = e_bikes.execute()
    result = []
    for i in query:
        result.append({"model_name": model_to_dict(i.model)["name"],
                       "color": i.color})
    return result


def get_e_bike_model_information(name):
    """
    get information of an e-bike model
    :param name: name of the e-bike model
    :return: information
    """
    info = EBikeModel.get(name=name)
    return model_to_dict(info)


def get_storage(name, color):
    """
    get storage of a certain e-bike model with a certain color
    :param name: name of the e-bike model
    :param color: color
    :return: storage
    """
    storage = EBike.select().where(
        EBike.model == name, EBike.color == color, EBike.status == "空闲"
    ).count()
    return storage


# ***************************** for test ***************************** #
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
    # print(get_available_e_bike_models())
    print(get_storage("E100小龟", "黄"))
