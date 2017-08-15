# -*- coding: UTF-8 -*-

"""
@author: larry.shuoren@outlook.com
@time: 8/10/17
@desc: battery rent service
"""

from datetime import datetime
from playhouse.shortcuts import model_to_dict

from server.service import serial_number_service
from server.database.model import Battery
from server.database.model import BatteryReport

from server.utility.exception import *

def add(**kwargs):
    """
    add new virtual card to database
    :param kwargs: parameters to insert to database
    :return:
    """
    serial_number = serial_number_service.get_available_battery_code()
    battery = Battery.create(
        serial_number=serial_number,
        **kwargs
    )
    return model_to_dict(battery)


def get_battery_rent_info(serial_number):
    """
    get battery rent information
    :param serial_number: battery id
    :return: information
    """
    # FIXME
    info = Battery.get(Battery.serial_number == serial_number)
    return model_to_dict(info)


def modify_use_status(**kwargs):
    """
    modify using status
    :param data: 
        b_id: battery id
        owner: user of battery
    :return: 
    """
    serial_number = kwargs["serial_number"]
    username = kwargs["username"]

    battery = Battery.get(serial_number=serial_number)
    if not battery.on_loan:
        raise Error("Battery is on loan")
    battery.on_loan = True
    battery.user = username
    return battery.save()

    # battery_info = Battery.get()
    # if battery_info:
    #     is_loan = model_to_dict(battery_info)["on_loan"]
    #     if is_loan:
    #         return "Battery is on loan"
    #     else:
    #         result = Battery.update(on_loan=True, user_id=owner
    #                                 ).where(Battery.serial_number == serial_number)
    #         result.execute()
    #         return "Modify succeed"
    # else:
    #     return "No battery found"


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
