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


def get_battery_rent_info(b_id):
    """
    get battery rent information
    :param b_id: battery id
    :return: information
    """
    # FIXME
    info = Battery.get(id=b_id)
    return model_to_dict(info)


def modify_use_status(b_id, owner):
    """
    modify using status
    :param b_id: battery id
    :param owner: user of battery
    :return:
    """
    battery_info = Battery.get(id=b_id)
    if battery_info:
        is_loan = model_to_dict(battery_info)["on_loan"]
        if is_loan:
            return "Battery is on loan"
        else:
            result = Battery.update(on_loan=True, user_id=owner).where(Battery.get_id == b_id)
            result.execute()
            return "Modify succeed"
    else:
        return "No battery found"


def add_repair_report(b_id, owner):
    """
    apply a repair report
    :param b_id: battery id
    :param owner: user of battery
    :return:
    """
    battery_info = model_to_dict(Battery.get(id=b_id))
    if battery_info["owner"] != owner:
        return "Owner not matched"
    BatteryReport.create(battery_id=b_id, current_owner=owner,
                         report_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
