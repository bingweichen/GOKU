"""

@author: Bingwei Chen

@time: 8/4/17

@desc: const


"""
from server.utility.constant.const_db import Const


def add(key, value, label):
    return Const.create(
        key=key,
        value=value,
        label=label
    )


def get_all():
    return Const.select()


def get(key):
    return Const.get(key=key)


def modify(key, value):
    const = Const.get(key=key)
    const.value = value
    return const.save()


def add_template():
    template_json = {
        "DEFAULT_DEPOSIT": 199.0,
        "MAXIMUM_APPOINTMENT": 5,
        "APPOINTMENT_EXPIRED_DAYS": 7,
        "BATTERY_RENT_PRICE": 1,
        "DEFAULT_APPOINTMENT_FEE": 100,
        "RENT_DEPOSIT": 1000

    }

    translate = {
        "DEFAULT_DEPOSIT": "默认押金",
        "MAXIMUM_APPOINTMENT": "最大订单数",
        "APPOINTMENT_EXPIRED_DAYS": "订单有效期",
        "BATTERY_RENT_PRICE": "电池租用价格",
        "DEFAULT_APPOINTMENT_FEE": "默认订单押金",
        "RENT_DEPOSIT": "默认租车订单押金"

    }

    for attr, value in template_json.items():
        label = translate[attr]
        add(attr, value, label)


if __name__ == "__main__":
    add_template()
