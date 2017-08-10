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

from playhouse.shortcuts import model_to_dict
from datetime import datetime

from server.database.model import Appointment
from server.service.storage_service import check_storage, decrement_num


def add(**kwargs):
    """
    add appointment

    eg = {

    "user": "bingwei",
    "e_bike_model": "E101小龟",
    "color": 蓝,
    "date": "datetime.now()",
    "note": "小龟电动车",
    "type": "小龟"
    }

    :param kwargs:
    :type kwargs:
    :return: the added json
    :rtype: json
    """
    appointment = Appointment.create(**kwargs)
    return model_to_dict(appointment)


def add_appointment(**kwargs):
    e_bike_model = kwargs["e_bike_model"]
    color = kwargs["color"]

    # 检查库存量，虽然库存不足时前端会生不成订单
    if not check_storage(model=e_bike_model, color=color):
        return
    appointment = Appointment.create(**kwargs)
    decrement_num(e_bike_model)
    return model_to_dict(appointment)


def get(*query, **kwargs):
    appointment = Appointment.get(*query, **kwargs)
    return model_to_dict(appointment)


def get_all():
    appointments = Appointment.select()
    new_appointments = []
    for appointment in appointments:
        new_appointments.append(model_to_dict(appointment))
    return new_appointments


def get_all_paginate(offset, limit):
    appointments = Appointment.select().paginate(offset, limit)
    new_appointments = []
    for appointment in appointments:
        new_appointments.append(model_to_dict(appointment))
    return new_appointments


def get_by_id(appointment_id):
    return model_to_dict(Appointment.get(Appointment.id == appointment_id))


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


# def test():
#
#     def tt2(user, *args, **kwargs):
#         print("1", user)
#
#     def tt(**data1):
#         print("xx", data1)
#         tt2(data1)
#         # print(**data1)
#         # print("1", data1["user"])
#
#     data = {
#         "user": "bingwei",
#         "e_bike_model": "E101小龟",
#         "color": "蓝",
#         "date": "datetime.now()",
#         "note": "小龟电动车",
#         "type": "小龟"
#     }
#     tt(**data)

# ***************************** unit test ***************************** #
def add_template():
    template_json = [
        {
            "user": "bingwei",
            "e_bike_model": "E101小龟",
            "color": "蓝",
            "date": datetime.now(),

            "type": "小龟"

        }
    ]
    for json in template_json:
        result = add(**json)
        print(result)


if __name__ == '__main__':
    pass

