# -*- coding: UTF-8 -*-

"""
@author: larry.shuoren@outlook.com
@time: 8/10/17
@desc: battery rent service
"""

from datetime import datetime
from playhouse.shortcuts import model_to_dict

from server.database.model import Battery
from server.database.model import BatteryReport
# from server.utility.json_utility import models_to_json


def add(**kwargs):
    """
    add new virtual card to database
    :param kwargs: parameters to insert to database
    :return:
    """
    battery = Battery.create(**kwargs)
    return model_to_dict(battery)


def get_battery_rent_info(b_id):
    """
    get battery rent information
    :param b_id: battery id
    :return: information
    """
    # FIXME
    info = Battery.get(Battery.id == b_id)
    return model_to_dict(info)


def modify_use_status(data):
    """
    modify using status
    :param data: 
        b_id: battery id
        owner: user of battery
    :return: 
    """
    b_id = data["b_id"]
    owner = data["owner"]
    battery_info = Battery.get(Battery.id == b_id)
    if battery_info:
        is_loan = model_to_dict(battery_info)["on_loan"]
        if is_loan:
            return "Battery is on loan"
        else:
            result = Battery.update(on_loan=True, user_id=owner
                                    ).where(Battery.id == b_id)
            result.execute()
            return "Modify succeed"
    else:
        return "No battery found"


def add_repair_report(data):
    """
    apply a repair report
    :param data: 
        b_id: battery id
        owner: user of battery
    :return:
    """
    b_id = data["b_id"]
    owner = data["owner"]
    battery_info = model_to_dict(Battery.get(Battery.id == b_id))
    if battery_info["owner"] != data["owner"]:
        return "Owner not matched"
    BatteryReport.create(battery=b_id, current_owner=owner,
                         report_time=datetime.now())
    return "Report succeed"


if __name__ == "__main__":
    # add(on_loan=True, desc="test", user="Shuo_Ren")
    print("hello world!")
    print(get_battery_rent_info(1))
