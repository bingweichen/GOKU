"""

@author: Bingwei Chen

@time: 2017.08.07

@desc: service for appointment

1. appointment Add/Get/Modify/Remove

1. get by id
2. get by user
3. get by e_bike_model

4. remove by id

5. modify status
"""

from datetime import datetime
from datetime import timedelta

from server.database.model import Appointment
from server.service import storage_service
from server.service import serial_number_service
from server.service import e_bike_model_service
from server.utility.exception import NoStorageError, WrongSerialsNumber
from server.utility.constant import *


def add(**kwargs):
    """
    add appointment

    eg = {
    "user": "bingwei",
    "e_bike_model": "小龟电动车 爆款 48V、12A",
    "color": 蓝,
    "note": "小龟电动车",
    "category": E_BIKE_MODEL_CATEGORY["0"],
    }

    :param kwargs:
    :type kwargs:
    :return: the added json
    :rtype: json
    """
    # 生成到期时间
    date = datetime.now()
    expired_date_time = date + timedelta(days=APPOINTMENT_EXPIRED_DAYS)

    appointment = Appointment.create(
        date=date, expired_date_time=expired_date_time, **kwargs)
    return appointment


# ***************************** buy appointment ***************************** #
# 1.生成订单
def add_appointment(**kwargs):
    e_bike_model = kwargs["e_bike_model"]
    color = kwargs["color"]
    # 检查库存量，虽然库存不足时前端会生不成订单
    if not storage_service.check_storage(model=e_bike_model, color=color):
        raise NoStorageError("not enough storage")

    # 检查该用户是否存在订单 (买车订单数）
    if not check_user_appointment(user=kwargs["user"]):
        raise NoStorageError("too much appointment")
    appointment = add(**kwargs)
    # 库存-1
    storage_service.decrement_num(e_bike_model, color)

    # 获取有效的 serial_number
    serial_number = serial_number_service.get_available_code(appointment)
    # 更改 serial_number
    appointment.serial_number = serial_number
    # 使用优惠劵
    # price = e_bike_model_service.get(name=e_bike_model).price

    appointment.save()
    return appointment


# 2. 预付款成功
def appointment_payment_success(appointment_id):
    status = APPOINTMENT_STATUS["1"]

    # # 预付款后更改新的过期日期
    # query = Appointment.update(
    #     status=status,
    #     expired_date_time=datetime.now+timedelta(days=APPOINTMENT_EXPIRED_DAYS)
    # ).where(
    #     Appointment.id == appointment_id
    # ).execute()

    return modify_status(appointment_id, status)


#  提车码
def upload_serial_number(appointment_id, serial_number):
    appointment = get(id=appointment_id)
    if check_serial_number(appointment, serial_number):
        return True
        # status = APPOINTMENT_STATUS["2"]
        # return modify_status(appointment_id, status)
    raise WrongSerialsNumber("wrong serials number")


# 4. 付款成功
def total_payment_success(appointment_id):
    # 检查是否租车
    appointment = get(id=appointment_id)
    if appointment.category == E_BIKE_MODEL_CATEGORY["2"]:  # 租车
        rent_time_period = appointment.rent_time_period
        end_time = datetime.now + \
                   timedelta(days=RENT_TIME_PERIOD[rent_time_period])
        appointment.end_time = end_time
        status = APPOINTMENT_STATUS["3"]
        appointment.status = status
        return appointment.save()

    status = APPOINTMENT_STATUS["4"]
    return modify_status(appointment_id, status)


# 取消订单
def cancel_appointment(appointment_id):
    appointment = get(id=appointment_id)
    # 退还押金
    return_appointment_fee(appointment)
    # 更改 serial number
    serial_number_service.modify_available_appointment(
        appointment.serial_number, True, None
    )
    # 退还库存
    status = APPOINTMENT_STATUS["-1"]
    increment_storage(appointment_id)
    return modify_status(appointment_id, status)


# 订单过期
def expired_appointment(appointment_id):
    status = APPOINTMENT_STATUS["-2"]
    increment_storage(appointment_id)
    return modify_status(appointment_id, status)


# 退还押金！！！
def return_appointment_fee(appointment):
    appointment_fee = appointment.appointment_fee
    if appointment_fee == 0:
        return
    print("需退还押金" + appointment_fee)


# 退还库存
def increment_storage(appointment_id):
    appointment = get(id=appointment_id)
    storage_service.increment_num(
        model=appointment.e_bike_model,
        color=appointment.color
    )


# 检查提车码
def check_serial_number(appointment, serial_number):
    if appointment.serial_number == serial_number:
        return True
    return False


def get(*query, **kwargs):
    # 检查是否过期
    appointment = Appointment.get(*query, **kwargs)
    if not check_valid(appointment):
        # 设置过期状态
        print(expired_appointment(appointment.id))
        appointment = Appointment.get(*query, **kwargs)
    return appointment


def get_all():
    appointments = Appointment.select()
    new_appointments = []
    for appointment in appointments:
        new_appointments.append(appointment)
    return new_appointments


def get_all_paginate(offset, limit):
    appointments = Appointment.select().paginate(offset, limit)
    new_appointments = []
    for appointment in appointments:
        new_appointments.append(appointment)
    return new_appointments


def get_by_id(appointment_id):
    return get(Appointment.id == appointment_id)


def modify_status(appointment_id, status):
    """

    :param appointment_id:
    :type appointment_id:
    :param status:
    :type status:
    :return:
    :rtype:
    """
    query = Appointment.update(
        status=status
    ).where(
        Appointment.id == appointment_id
    )
    return query.execute()


def remove_by_id(appointment_id):
    query = Appointment.delete().where(Appointment.id == appointment_id)
    return query.execute()


def check_user_appointment(user):
    count = Appointment.select().where(
        Appointment.user == user).count()
    if count >= MAXIMUM_APPOINTMENT:
        return False
    else:
        return True


def check_valid(appointment):
    """

    :param appointment:
    :type appointment:
    :return: True is valid
    :rtype: bool
    """
    now = datetime.now()
    if now >= appointment.expired_date_time:
        return False
    else:
        return True


# ***************************** rent appointment ***************************** #
# 1.生成租车订单
def add_rent_appointment(**kwargs):


    pass


# ***************************** unit test ***************************** #
def add_template():
    template_json = [
        {
            "user": "bingwei",
            "e_bike_model": "小龟电动车 爆款 48V、12A",
            "color": "蓝",
            "category": E_BIKE_MODEL_CATEGORY["0"],
        }
    ]
    for json in template_json:
        result = add(**json)
        print(result)


if __name__ == '__main__':
    print(Appointment.get(Appointment.id == 1))
    # print(add_template())
    pass
