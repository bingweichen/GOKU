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

from server.database.model import Appointment, EBikeModel
from server.service import storage_service
from server.service import serial_number_service
from server.service import virtual_card_service
from server.service import coupon_service
from server.service import refund_table_service

# from server.service import e_bike_model_service

from server.utility.exception import WrongSerialsNumber, Error

from server.utility.constant.basic_constant import *
from server.utility.constant.custom_constant import get_custom_const


# from server.utility.json_utility import models_to_json


# ***************************** buy appointment ***************************** #
# 1.生成订单
def add_appointment(**kwargs):
    user = kwargs["user"]
    e_bike_model = kwargs["e_bike_model"]
    color = kwargs["color"]
    e_bike_type = kwargs["type"]
    coupon = kwargs.get("coupon")
    rent_time_period = kwargs.get("rent_time_period")

    e_bike_model = EBikeModel.get(name=e_bike_model)

    # 检查库存量，虽然库存不足时前端会生不成订单
    if not storage_service.check_storage(model=e_bike_model, color=color):
        raise Error("not enough storage")

    # 检查该用户是否存在订单 (买车订单数）
    if not check_user_appointment(user=user, type=e_bike_type):
        raise Error("too much appointment")

    # 租车订单 检查是否存在押金
    if e_bike_type == "租车":
        if not virtual_card_service.check_deposit(username=user):
            raise Error("no deposit in virtual_card")

    if e_bike_type == "租车":
        price = e_bike_model.price[rent_time_period]
    else:
        price = e_bike_model.price

    # 库存-1
    storage_service.decrement_num(e_bike_model, color)

    # 使用优惠劵
    if coupon:
        reduced_price = coupon_service.use_coupon(user, coupon, price)
        price = price - reduced_price
        kwargs["reduced_price"] = reduced_price
    kwargs["price"] = price
    appointment = add(**kwargs)

    # 获取有效的 serial_number
    serial_number = serial_number_service.get_available_code(appointment)
    # 更改 serial_number
    appointment.serial_number = serial_number
    appointment.save()
    return appointment


# 2. 预付款成功
def appointment_payment_success(user, appointment_id):
    appointment = Appointment.get(
        id=appointment_id,
        user=user)
    appointment.status = APPOINTMENT_STATUS["1"]
    # 预付款后更改新的过期日期
    appointment.expired_date_time = \
        datetime.now() + timedelta(
            days=get_custom_const("APPOINTMENT_EXPIRED_DAYS"))
    return appointment.save()


# 3. 提车码
def upload_serial_number(user, appointment_id, serial_number):
    appointment = get(id=appointment_id, user=user)
    if check_serial_number(appointment, serial_number):
        return True
    raise WrongSerialsNumber("wrong serials number")


# 4. 付款成功
def total_payment_success(user, appointment_id):
    appointment = Appointment.get(
        id=appointment_id,
        user=user)

    # 检查是否租车
    if appointment.type == "租车":  # 租车
        rent_time_period = appointment.rent_time_period
        end_time = \
            datetime.now() + timedelta(days=RENT_TIME_PERIOD[rent_time_period])
        appointment.end_time = end_time
        status = RENT_APPOINTMENT_STATUS["2"]
        appointment.status = status
        return appointment.save()

    else:
        status = APPOINTMENT_STATUS["3"]
        appointment.status = status
        return appointment.save()


# 取消订单
def cancel_appointment(appointment_id, username=None, **kwargs):
    appointment = Appointment.get(id=appointment_id)
    if username and username != appointment.user:
        raise Exception("not your appointment")

    terminate_appointment(appointment_id, appointment, **kwargs)

    appointment.status = APPOINTMENT_STATUS["-1"]
    result = appointment.save()
    return result


# 订单过期
def expired_appointment(appointment_id):
    appointment = Appointment.get(id=appointment_id)

    terminate_appointment(
        appointment_id,
        appointment,
        account="",
        account_type="",
        comment=""
    )

    appointment.status = APPOINTMENT_STATUS["-2"]
    return appointment.save()


# 退还押金！！！
def return_appointment_fee(username, appointment, **kwargs):
    appointment_fee = appointment.appointment_fee
    if appointment_fee == 0:
        return

    refund_table_service.add(
        user=username,
        account=kwargs["account"],
        account_type=kwargs["account_type"],
        type="退预约金",
        value=appointment_fee,
        comment=kwargs["comment"]
    )
    print("需退还押金" + appointment_fee)


# 退还库存
def increment_storage(appointment_id):
    appointment = Appointment.get(id=appointment_id)
    result = storage_service.increment_num(
        model=appointment.e_bike_model,
        color=appointment.color
    )
    return result


# 检查提车码
def check_serial_number(appointment, serial_number):
    if appointment.serial_number == serial_number:
        return True
    return False


# 检查用户订单数量
def check_user_appointment(user, type):
    count = Appointment.select().where(
        Appointment.user == user,
        Appointment.type == type,
        ~(Appointment.status << [APPOINTMENT_STATUS["-1"],
                                 APPOINTMENT_STATUS["-2"],
                                 APPOINTMENT_STATUS["3"]
                                 ])
    ).count()
    if type == "租车":
        if count >= 1:
            return False
        else:
            return True
    if count >= get_custom_const("MAXIMUM_APPOINTMENT"):
        return False
    else:
        return True


# 检查订单有效时间
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
# def add_rent_appointment(**kwargs):
#     # 检查该用户是否有押金
#     username = kwargs["username"]
#     e_bike_model = kwargs["e_bike_model"]
#     color = kwargs["color"]
#     type = kwargs["type"]
#
#     coupon = kwargs.get("coupon")
#
#     if not virtual_card_service.check_deposit(username):
#         raise Error("no deposit")
#
#     # 检查库存量，虽然库存不足时前端会生不成订单
#     if not storage_service.check_storage(model=e_bike_model, color=color):
#         raise Error("not enough storage")
#
#     # 检查该用户是否存在订单 (租车订单数）
#     if not check_user_appointment(user=kwargs["user"], type=type):
#         raise Error("too much appointment")
#
#     appointment = add(**kwargs)
#     # # 库存-1
#     storage_service.decrement_num(e_bike_model, color)
#
#     # 使用优惠劵
#     # price = e_bike_model_service.get(name=e_bike_model).price
#     price = appointment.e_bike_model.price
#     if coupon:
#         reduced_price = coupon_service.use_coupon(username, coupon, price)
#         price = price - reduced_price
#         appointment.reduced_price = reduced_price
#     appointment.price = price
#     appointment.save()
#     return appointment
#     pass


# 4. 用户还车，由管理员执行
def return_e_bike(appointment_id, serial_number, **kwargs):
    appointment = Appointment.get(id=appointment_id)
    if not check_serial_number(
            serial_number=serial_number,
            appointment=appointment):
        raise Error("wrong serial number")

    appointment.status = RENT_APPOINTMENT_STATUS["3"]
    result = appointment.save()
    terminate_appointment(appointment_id, appointment, **kwargs)
    return result


# ***************************** general ***************************** #
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
    expired_date_time = date + timedelta(
        days=get_custom_const("APPOINTMENT_EXPIRED_DAYS"))

    appointment = Appointment.create(
        date=date, expired_date_time=expired_date_time, **kwargs)
    return appointment


def get(*query, **kwargs):
    # 检查是否过期
    appointment = Appointment.get(*query, **kwargs)
    if not check_valid(appointment):
        # 设置过期状态
        print(expired_appointment(appointment.id))
        appointment = Appointment.get(*query, **kwargs)
    return appointment


def get_all(username=None):
    if username:
        appointments = Appointment.select().where(
            Appointment.user == username,
        )
    else:
        appointments = Appointment.select()
    return appointments


def manager_get(type, period, **kwargs):
    today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    before = today - timedelta(days=period)

    appointments = Appointment.select().where(
        Appointment.type == type,
        Appointment.date >= before
    ).paginate(
        offset=kwargs["offset"],
        limit=kwargs["limit"])
    return appointments


def get_all_paginate(offset, limit):
    appointments = Appointment.select().paginate(offset, limit)
    new_appointments = []
    for appointment in appointments:
        new_appointments.append(appointment)
    return new_appointments


def get_by_id(appointment_id, username=None):
    if username:
        return get(
            Appointment.id == appointment_id,
            Appointment.user == username
        )
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


def count():
    return Appointment.select().count()


def terminate_appointment(appointment_id, appointment, **kwargs):
    # 增加库存
    increment_storage(appointment_id)
    # 更改 serial number
    serial_number_service.modify_available_appointment(
        code=appointment.serial_number,
        available=True,
        appointment=None
    )
    # 退还押金
    username = appointment.user
    return_appointment_fee(
        username,
        appointment,
        **kwargs
    )


# ***************************** unit test ***************************** #
def add_template():
    template_json = [
        {
            "username": "bingwei",

            "e_bike_model": "小龟电动车 爆款 48V、12A",
            "color": "蓝",
            "category": "小龟",
            "type": "买车",
            "note": "",
            "coupon": None
        }
    ]
    for json in template_json:
        result = add(**json)
        print(result)


if __name__ == '__main__':
    # print(models_to_json(
    #     Appointment.select().where(Appointment.category == None)))
    # print(Appointment.get(Appointment.id == 1))
    # print(add_template())
    pass
