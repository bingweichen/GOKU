"""

@author: Bingwei Chen

@time: 8/4/17

@desc: const


"""
from server.database.model import Const


def add(key, value):
    return Const.create(
        key=key,
        value=value
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
    }
    for attr, value in template_json.items():
        add(attr, value)


if __name__ == "__main__":
    add_template()
