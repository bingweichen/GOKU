# -*- coding: UTF-8 -*-

"""
@author: bingweiChen

@time: 8/10/17
@desc: battery report
"""

from datetime import datetime, timedelta

from server.database.model import BatteryReport


# def get_all(username=None):
#     if username:
#         battery_record = BatteryReport.select().where(
#             BatteryReport.current_owner==username
#         )
#         return battery_record


def get_all_paginate():
    return BatteryReport.select()
    # if period == 0:
    #     battery_record = BatteryReport.select()
    # else:
    #     if period > 0:
    #         period -= 1
    #
    #     today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    #     before = today - timedelta(days=period)
    #     battery_record = BatteryReport.select().where(
    #         BatteryReport.report_time >= before
    #     )
    # return battery_record
