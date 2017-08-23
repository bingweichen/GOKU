# -*- coding: UTF-8 -*-

"""
@author: bingweiChen

@time: 8/10/17
@desc: battery rent service
"""

from datetime import datetime, timedelta

from server.service import serial_number_service
from server.service import virtual_card_service

from server.database.model import BatteryRecord

from server.utility.exception import *
from server.utility.constant.custom_constant import get_custom_const


def get_all(username=None):
    if username:
        battery_record = BatteryRecord.select().where(
            user=username
        )
        return battery_record
    battery_record = BatteryRecord.select()
    return battery_record

