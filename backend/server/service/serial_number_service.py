from playhouse.shortcuts import model_to_dict
from server.service import store_service
from server.database.model import SerialNumber

"""
1」学校代码：【浙大为A】、【浙工大、万向职业技术学院、浙江外国语学院为B】、【浙江科技学院、长征职业技术学院为C】
2」业务代码：买车为M、租车的代码为Z（mini租特殊，为P）闪充没有业务代码（只有区域代码，方便区分投放区域）
3」编号类型：买车（学校代码+业务类型+四位数字）、租车（学校代码+业务类型+四位数字）、闪充（学校代码+五位数字）
4」数字规则：四位数按照0001到9999依次排序，五位数按照00001到99999依次排序。（租车、买车）用户预约和租买就占用一个数字，数字依次增大，若中途某个订单取消则这个数字后续继续使用，依然按照自然数字大小。线下实体店提车时需输入数字进行信息匹配（参照前端），并把已经打印好匹配的车牌等装到用户车身。数字一人一个一定不要重复。
5」编号举例：浙大学生买车：AM0001、浙工大租车：BZ0001、闪充编号：A00001、B00001
"""
STORE_CODE = {
    "浙大Goku出行": "A",
    "浙工大Goku出行": "B",
    "浙科院Goku出行": "C",
}

E_BIKE_MODEL_TYPE_CODE = {
    "买车": "M",
    "租车": "Z",
    "MINI租": "P"
}


def get_all(page, paginate_by):
    total = SerialNumber.select().count()
    serial_number = SerialNumber.select().paginate(
        page=page, paginate_by=paginate_by)
    return serial_number, total


def get_available_code(appointment):
    store = appointment.user.school.store
    type = appointment.type
    category_code = E_BIKE_MODEL_TYPE_CODE[type]
    if appointment.category == "MINI租":
        category_code = E_BIKE_MODEL_TYPE_CODE[appointment.category]
    serial_number = SerialNumber.get(
        store=store,
        category_code=category_code,
        available=True
    )
    # 更改被使用的serial number
    serial_number.available = False
    serial_number.appointment = appointment
    serial_number.save()
    code = serial_number.code
    return code


def get_available_battery_code():
    serial_number = SerialNumber.select().where(
        SerialNumber.category_code == None,
        # SerialNumber.category_code.not_in(["M", "Z", "P"]),
        SerialNumber.available == True).get()

    # 更改被使用的serial number
    serial_number.available = False
    # serial_number.battery = battery
    serial_number.save()
    return serial_number.code


# 更改被使用的serial number
def modify_available_appointment(code, available, appointment):
    query = SerialNumber.update(
        available=available,
        appointment=appointment
    ).where(
        SerialNumber.code == code
    )
    return query.execute()
    pass


# def get_code(appointment):
#     """
#
#     :param appointment:
#     :type appointment:
#     :return:
#     :rtype:
#     """
#     store = appointment.user.school.store
#     store_code = STORE_CODE[store]
#
#     category = appointment.category
#     category_code = E_BIKE_MODEL_CATEGORY[category]
#
#     pass


def get_empty_code(store_code, category_code):
    pass


REQUIREMENTS = [
    {
        "key": "A",
        "store": "浙大Goku出行",
        "value": [
            {
                "key": "M",
                "value": [1, 101]
            },
            {
                "key": "Z",
                "value": [1, 101]
            },
            {
                "key": "P",
                "value": [1, 21]
            }
        ]
    },

    {
        "key": "B",
        "store": "浙工大Goku出行",
        "value": [
            {
                "key": "M",
                "value": [1, 201]
            },
            {
                "key": "Z",
                "value": [1, 201]
            },
            {
                "key": "P",
                "value": [1, 51]
            }
        ]
    },

    {
        "key": "C",
        "store": "浙科院Goku出行",
        "value": [
            {
                "key": "M",
                "value": [1, 201]
            },
            {
                "key": "Z",
                "value": [1, 201]
            },
            {
                "key": "P",
                "value": [1, 51]
            }
        ]
    }
]


def generate_by_requirement():
    for req in REQUIREMENTS:
        store = store_service.get(name=req["store"])
        store_code = STORE_CODE[store.name]
        for category in req["value"]:
            category_code = category["key"]
            for i in range(
                    int(category["value"][0]),
                    int(category["value"][1])):
                e_bike_code = str(i).zfill(4)
                serial_number = SerialNumber.create(
                    code=store_code + category_code + e_bike_code,
                    store=store.name,
                    store_code=store_code,
                    category_code=category_code
                )
                print(serial_number)


BATTERY_REQUIREMENT = [
    {
        "key": "A",
        "store": "浙大Goku出行",
        "value": [1, 201]
    },
    {
        "key": "B",
        "store": "浙工大Goku出行",
        "value": [1, 301]
    },
    {
        "key": "C",
        "store": "浙科院Goku出行",
        "value": [1, 301]
    },
]


def generate_battery_serial_number():
    for req in BATTERY_REQUIREMENT:
        store = store_service.get(name=req["store"])
        store_code = STORE_CODE[store.name]
        for i in range(
                int(req["value"][0]),
                int(req["value"][1])):
            battery_code = str(i).zfill(5)
            serial_number = SerialNumber.create(
                code=store_code + battery_code,
                store=store.name,
                store_code=store_code,
            )
            print(serial_number)
    #
    # stores = store_service.get_all()
    # for store in stores:
    #     store_code = STORE_CODE[store.name]
    #     # 电池序列号
    #     for i in range(1, 201):
    #         battery_code = str(i).zfill(5)
    #         serial_number = SerialNumber.create(
    #             code=store_code + battery_code,
    #             store=store.name,
    #             store_code=store_code,
    #         )
    #         print(serial_number)


def set_available_to_false():
    result = SerialNumber.update(avaiable=False)
    return result


# ***************************** test ***************************** #
def get_available_code_t():
    from server.service import appointment_service
    appointment = appointment_service.get_by_id(6)
    get_available_code(appointment)


if __name__ == "__main__":
    pass
    print(generate_battery_serial_number())
    generate_by_requirement()
    # generate_serial_number()
