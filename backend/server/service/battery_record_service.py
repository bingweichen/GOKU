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


def get_all_paginate(page, paginate_by, period,  **kwargs):
    serial_number = kwargs["serial_number"]
    battery_record = BatteryRecord.select()

    if period > 0:
        period -= 1
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        before = today - timedelta(days=period)
        battery_record = battery_record.where(
            BatteryRecord.rent_date >= before
        )

    if serial_number:
        battery_record = battery_record.where(
            BatteryRecord.battery.regexp(kwargs["serial_number"])
        )

    total = battery_record.count()
    battery_record = battery_record.order_by(BatteryRecord.id.desc())
    battery_record = battery_record.paginate(page=page, paginate_by=paginate_by)
    return battery_record, total


def add_record(username, battery):
    BatteryRecord.create(
        rent_date=datetime.utcnow(),
        battery=battery,
        user=username
    )


def get(*query, **kwargs):
    battery_record = BatteryRecord.get(*query, **kwargs)
    # battery_record = BatteryRecord.select().where(*query, **kwargs)\
    #     .order_by(BatteryRecord.id).get()

    return battery_record


