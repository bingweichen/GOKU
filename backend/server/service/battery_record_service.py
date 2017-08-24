# -*- coding: UTF-8 -*-

"""
@author: bingweiChen

@time: 8/10/17
@desc: battery rent service
"""

from datetime import datetime, timedelta

from server.database.model import BatteryRecord


def get_all(username=None):
    if username:
        battery_record = BatteryRecord.select().where(
            BatteryRecord.user==username
        )
        return battery_record
    battery_record = BatteryRecord.select()
    return battery_record


def add_record(username, battery):
    BatteryRecord.create(
        rent_date=datetime.utcnow(),
        battery=battery,
        user=username
    )