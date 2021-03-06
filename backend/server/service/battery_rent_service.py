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
from server.service import battery_record_service

from server.database.model import Battery
from server.database.model import BatteryRecord
from server.database.model import BatteryReport
from server.database.model import User

from server.utility.exception import *
from server.utility.constant.custom_constant import get_custom_const
from server.utility.constant.basic_constant import BasicConstant


# ***************************** service ***************************** #
def get_all_paginate(page, paginate_by, **kwargs):
    battery = Battery.select()
    serial_number = kwargs["serial_number"]
    if serial_number:
        battery = battery.\
            where(Battery.serial_number.regexp(kwargs["serial_number"]))

    total = battery.count()
    battery = battery.paginate(page=page, paginate_by=paginate_by)
    return battery, total


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


#

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

    battery = Battery.get(serial_number=serial_number)
    # 检查是否已经租用电池
    if check_user_on_load(username):
        raise Error("还未归还电池")
    # 检查电池状态
    if battery.on_loan:
        raise Error("电池已被租用")

    # 检查账户状态
    virtual_card_service.check_status(username)

    battery.on_loan = True
    battery.user = username
    battery_record_service.add_record(username, battery)
    return battery.save()


# 归还电池
def return_battery(username, serial_number):
    battery = Battery.get(serial_number=serial_number)

    # 通过电池，找到借用中电池记录
    battery_records = battery.battery_records
    battery_record = get_using_record(battery_records)
    battery_record.return_date = datetime.utcnow()

    # 30分钟内不允许归还
    if convert_timedelta(
                    battery_record.return_date - battery_record.rent_date)\
            < BasicConstant.battery_return_min_minutes:
        raise Error("%s分钟内无法归还" % BasicConstant.battery_return_min_minutes)

    # 扣款计算
    price = calculate_price(battery_record.rent_date,
                            battery_record.return_date)
    battery_record.price = price
    battery_record.situation = "已归还"

    # 更改电池状态
    battery.on_loan = False
    battery.user = None

    battery.save()
    battery_record.save()
    # 扣款
    virtual_card_service.consume_virtual_card(
        card_no=username,
        amount=price)

    # 当超出一个月归还，冻结账户
    delta = battery_record.return_date - battery_record.rent_date
    if delta > timedelta(days=BasicConstant.maximum_rent_days):
        result = virtual_card_service.freeze(battery_record.user, "电池租用超一月")
        print("result", result)

    return battery_record


# def check_on_load_batter_rent_date(username):
#     """
#
#     :param username:
#     :type username:
#     :return: False 超出租用限制
#     :rtype:
#     """
#     battery = Battery.get(user=username)
#
#     # battery = Battery.get(serial_number=serial_number)
#     battery_records = battery.battery_records
#     battery_record = get_using_record(battery_records)
#     rent_date = battery_record.rent_date
#     now = datetime.utcnow()
#     if (now - rent_date).days > 31:
#         return False
#     return True


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


def manager_get_total_uses_amount():
    total_number = int(BatteryRecord.select().count())
    return total_number or 0


def manager_get_current_uses_amount():
    current_use = int(BatteryRecord.select().where(
        BatteryRecord.situation == "借用中").count())
    return current_use or 0


# # 获取电池
# def manager_get_battery(serial_number):
#     battery = Battery.get(serial_number=serial_number)
#     return battery
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
        BatteryRecord.rent_date >= before)
    return record


def calculate_price(rent_date, return_date):
    """
    两周内1元
    超过两周，每天扣2元

    超过 1个月 冻结账户以实现在脚本中


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
    if days >= BasicConstant.maximum_normal_rent_price_days:
        price = price + (days - BasicConstant.maximum_normal_rent_price_days) \
                        * BasicConstant.abnormal_rent_price_per_day
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
    # add_script()
