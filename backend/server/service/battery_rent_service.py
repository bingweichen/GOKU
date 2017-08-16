# -*- coding: UTF-8 -*-

"""
@author: larry.shuoren@outlook.com
@time: 8/10/17
@desc: battery rent service
"""

from datetime import datetime, timedelta
from playhouse.shortcuts import model_to_dict

from server.service import serial_number_service
from server.service import virtual_card_service

from server.database.model import Battery
from server.database.model import BatteryRecord
from server.database.model import BatteryReport

from server.utility.exception import *
from server.utility.constant import *
from server.utility.json_utility import models_to_json


# ***************************** service ***************************** #
def get_battery(serial_number):
    """
    get battery rent information
    :param serial_number: battery id
    :return: information
    """
    battery = Battery.get(Battery.serial_number == serial_number)
    return battery


def get_user_battery(username):
    battery = Battery.get(Battery.user == username)
    return battery


def rent_battery(**kwargs):
    """
    modify using status
    :param kwargs:
        b_id: battery id
        owner: user of battery
    :return:
    """

    serial_number = kwargs["serial_number"]
    username = kwargs["username"]
    if not virtual_card_service.check_deposit(username):
        return
    battery = Battery.get(serial_number=serial_number)
    if battery.on_loan:
        raise Error("Battery is on loan")
    battery.on_loan = True
    battery.user = username

    add_record(battery)
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


# 归还电池
def return_battery(username, serial_number):
    battery = Battery.get(serial_number=serial_number)
    # 更改电池
    battery.on_loan = False
    battery.user = None
    battery.save()
    # 通过电池，找到借用中电池记录，更改状态
    battery_records = battery.battery_records
    battery_record = get_using_record(battery_records)
    battery_record.return_date = datetime.now()
    battery_record.price = BATTERY_RENT_PRICE
    battery_record.situation = "已归还"
    battery_record.save()
    # 扣款
    virtual_card_service.consume_virtual_card(
        card_no=username, amount=BATTERY_RENT_PRICE)
    return battery_record


def get_using_record(records):
    for record in records:
        if record.situation == "借用中":
            return record


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


def add_record(battery):
    BatteryRecord.create(
        rent_date=datetime.now(),
        battery=battery,
    )


def manager_get_total_uses_amount():
    total_number = int(BatteryRecord.select().count())
    return total_number or 0


def manager_get_current_uses_amount():
    current_use = int(BatteryRecord.select().where(
        BatteryRecord.situation == "借用中").count())
    return current_use or 0


def manager_get_use_status_by_id(serial_number):
    battery = Battery.select().where(Battery.serial_number == serial_number)
    loan = battery.on_loan
    if loan:
        user = battery.user_id
        return {"on_loan": True, "user": user}
    else:
        return {"on_loan": False}


def manager_get_history_record_by_id(serial_number, period):
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    before = today-timedelta(days=period)
    record = BatteryRecord.select().where(
        BatteryRecord.battery == serial_number,
        BatteryRecord.return_date >= before)
    record = models_to_json(record)
    return record


# def calculate_price(duration):
#     # 15分钟 1元
#     days, seconds = duration.days, duration.seconds
#     total_minutes = days*3600+seconds/60
#
#
# def convert_timedelta(duration):
#     days, seconds = duration.days, duration.seconds
#     print(days, seconds)
#     hours = seconds // 3600
#     minutes = (seconds % 3600) // 60
#     seconds = (seconds % 60)
#     return days, hours, minutes, seconds


if __name__ == "__main__":
    pass
    # rent_battery(username="bingwei", serial_number="A00001")
    return_battery("bingwei", "A00001")
    # add(on_loan=True, desc="test", user="Shuo_Ren")
    # print("hello world!")
    # print(get_battery_rent_info(1))
    # print(convert_timedelta(timedelta(0, 3600*24*100+30)))
