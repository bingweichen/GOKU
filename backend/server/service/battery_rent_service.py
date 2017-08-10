# -*- coding: UTF-8 -*-

"""
@author: larry.shuoren@outlook.com
@time: 8/10/17
@desc: battery rent service
"""

from playhouse.shortcuts import model_to_dict

from server.database.model import Battery
# from server.utility.json_utility import models_to_json


def get_battery_rent_info(b_id):
    info = Battery.select().where(Battery.b_id == b_id)
    return model_to_dict(info)

