# -*- coding: UTF-8 -*-

"""
@author: larry.shuoren@outlook.com
@author: bingweiChen

@time: 8/10/17
@desc: battery rent service
"""

from datetime import datetime, timedelta

from server.service import serial_number_service
from server.service import virtual_card_service

from server.database.model import Battery
from server.database.model import BatteryRecord
from server.database.model import BatteryReport
from server.database.model import User

from server.utility.exception import *
from server.utility.constant.custom_constant import get_custom_const


# from server.utility.json_utility import models_to_json
# from playhouse.shortcuts import model_to_dict


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
    battery_record = BatteryRecord.get(
        battery=battery,
        situation="借用中"
    )
    return battery, battery_record


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

    # 检查是否已经租用电池
    if check_user_on_load(username):
        raise Error("还未归还电池")
    if not virtual_card_service.check_deposit(username):
        raise Error("没有足够的押金")
    battery = Battery.get(serial_number=serial_number)
    if battery.on_loan:
        raise Error("电池已被租用")

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

    # 通过电池，找到借用中电池记录，更改状态
    battery_records = battery.battery_records
    battery_record = get_using_record(battery_records)
    battery_record.return_date = datetime.utcnow()
    # 扣款计算
    price = calculate_price(battery_record.rent_date,
                            battery_record.return_date)
    battery_record.price = price
    battery_record.situation = "已归还"

    # 30分钟内不允许归还
    if convert_timedelta(
                    battery_record.return_date - battery_record.rent_date) < 30:
        raise Exception("30分钟内无法归还")

    battery.save()
    battery_record.save()
    # 扣款
    virtual_card_service.consume_virtual_card(
        card_no=username,
        amount=price)
    return battery_record


def check_on_load_batter_rent_date(username):
    """

    :param serial_number:
    :type serial_number:
    :return: False 超出租用限制
    :rtype:
    """
    battery = Battery.get(user=username)

    # battery = Battery.get(serial_number=serial_number)
    battery_records = battery.battery_records
    battery_record = get_using_record(battery_records)
    rent_date = battery_record.rent_date
    now = datetime.utcnow()
    if (now - rent_date).days > 31:
        return False
    return True


def get_using_record(records):
    for record in records:
        if record.situation == "借用中":
            return record


# 添加电池
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
    return battery


def add_repair_report(serial_number):
    """
    apply a repair report
    :param serial_number:

    :return:
    """
    battery = Battery.get(serial_number=serial_number)
    return BatteryReport.create(
        battery=serial_number,
        current_owner=battery.user,
        report_time=datetime.utcnow()
    )


def add_record(battery):
    BatteryRecord.create(
        rent_date=datetime.utcnow(),
        battery=battery,
    )


def manager_get_total_uses_amount():
    total_number = int(BatteryRecord.select().count())
    return total_number or 0


def manager_get_current_uses_amount():
    current_use = int(BatteryRecord.select().where(
        BatteryRecord.situation == "借用中").count())
    return current_use or 0


# 获取相册
def manager_get_battery(serial_number):
    battery = Battery.select().where(Battery.serial_number == serial_number)
    return battery
    # loan = battery.on_loan
    # if loan:
    #     user = battery.user_id
    #     return {"on_loan": True, "user": user}
    # else:
    #     return {"on_loan": False}


def manager_get_history_record_by_id(serial_number, period):
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    before = today - timedelta(days=period)
    record = BatteryRecord.select().where(
        BatteryRecord.battery == serial_number,
        BatteryRecord.return_date >= before)
    return record


def calculate_price(rent_date, return_date):
    """
    两周内1元
    超过两周，每天扣2元


    :param rent_date:
    :type rent_date:
    :param return_date:
    :type return_date:
    :return:
    :rtype:
    """
    duration = return_date - rent_date
    days, seconds = duration.days, duration.seconds
    price = get_custom_const("BATTERY_RENT_PRICE")
    if days >= 14:
        price = price + (days - 14) * 2
    return price


# def calculate_price(duration):
#     # 15分钟 1元
#     days, seconds = duration.days, duration.seconds
#     total_minutes = days*3600+seconds/60
#
#
def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    total_minutes = days * 3600 + seconds / 60
    return total_minutes
    # print(days, seconds)
    # hours = seconds // 3600
    # minutes = (seconds % 3600) // 60
    # seconds = (seconds % 60)
    # return days, hours, minutes, seconds


# 添加电池脚本
def add_script():
    """
    add new virtual card to database
    :param kwargs: parameters to insert to database
    :return:
    """
    for count in range(0, 800):
        serial_number = serial_number_service.get_available_battery_code()
        battery = Battery.create(
            serial_number=serial_number,
        )
        print(count)
        print(battery)


# 现在使用的闪充
def get_on_load_battery(username=None):
    if username:
        battery = Battery.get(
            user=username,
            on_loan=True
        )
        return battery
    else:
        battery = Battery.select().where(
            Battery.on_loan == True
        )
        return battery


def check_user_on_load(username):
    user = User.get(username=username)
    battery = user.battery
    if battery:
        return True
    else:
        return False

if __name__ == "__main__":
    pass
    print(check_on_load("Bingwei"))
    # print(calculate_price(datetime(2017, 8, 1, 6), datetime(2017, 8, 16, 5)))
    # rent_battery(username="bingwei", serial_number="A00001")
    # return_battery("bingwei", "A00001")
    # add(on_loan=True, desc="test", user="Shuo_Ren")
    # print("hello world!")
    # print(get_battery_rent_info(1))
    # print(convert_timedelta(timedelta(0, 3600*24*100+30)))
