# -*- coding: UTF-8 -*-
"""

@author: Bingwei Chen

@time: 2017.07.20

@desc: service for store

1. store Add/Get/Modify/Remove

"""
from playhouse.shortcuts import model_to_dict

from server.database.model import Store


def add(**kwargs):
    """
    add store

    eg = {
    "name": "123456",
    "address": "bing"
    }

    :param kwargs:
    :type kwargs:
    :return: the added json
    :rtype: json
    """
    store = Store.create(**kwargs)
    return model_to_dict(store)


def get(*query, **kwargs):
    store = Store.get(*query, **kwargs)
    return model_to_dict(store)


def get_all():
    stores = Store.select()
    new_stores = []
    for store in stores:
        new_stores.append(model_to_dict(store))
    return new_stores


def get_by_name(name):
    return model_to_dict(Store.get(Store.name == name))


# 暂未启用
# def modify(search_query, modify_json):
#
#     q = Store.update(**modify_json).where(Store.registration_expired == True)
#
#     store = Store.get(**search_query)
#     store.update()
#     pass


def modify_by_name(name, modify_json):
    """

    :param name:
    :type name:
    :param modify_json:
    :type modify_json:
    :return: number of row update, 0 if not find, error if modify_json is wrong
    :rtype: int
    """
    query = Store.update(**modify_json).where(Store.name == name)
    return query.execute()


def remove_by_name(name):
    query = Store.delete().where(Store.name == name)
    return query.execute()


# ***************************** test ***************************** #
def add_test():
    """

    uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15), is_relative=True)
    uncle_bob.save() # bob is now stored in the database

    使用create成功
    grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1), is_relative=True)

    使用save失败 使用force_insert=True成功 因为没有primary key
    :return:
    :rtype:
    """
    store = Store.create(name="123456111", address="bing111")
    return model_to_dict(store)


def add_test_2():
    store = add(**{"name": "1234561112", "address": "bing1113"})
    print(store)


def get_test():
    """

    two way of get

    User.select().where(User.active == True).order_by(User.username)
    grandma = Person.get(Person.name == 'Grandma L.')

    :return:
    :rtype:
    """
    store = Store.get()
    print(model_to_dict(store))
    return store


def get_all_test():
    stores = Store.select()
    for store in stores:
        # for school in store.schools:
        #     print("school", model_to_dict(school))
        print(model_to_dict(store))
    return stores


def modify_test():
    """

    :return:
    :rtype:
    """
    # get
    q = Store.update(name="111").where(Store.id == "1")
    print(q.execute())


# ***************************** unit test ***************************** #
def add_template():
    template_json = [
        {
            "name": "浙大Goku出行",
            "address": "浙大"
        },
        {
            "name": "浙工大Goku出行",
            "address": "浙工大"
        },
        {
            "name": "浙科院Goku出行",
            "address": "浙科院"
        }
    ]
    for json in template_json:
        result = add(**json)
        print(result)


if __name__ == '__main__':
    pass
    add_template()
