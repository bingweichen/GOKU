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


# def get(key):
#     return Const.get(key=key)


def modify(key, value):
    const = Const.get(key=key)
    const.value = value
    return const.save()


# def add_template():
