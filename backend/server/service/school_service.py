# -*- coding: UTF-8 -*-
"""

@author: Bingwei Chen

@time: 2017.07.20

@desc: service for school

1. school Add/Get/Modify/Remove

浙江大学、浙江工业大学、浙江科技学院、浙江外国语学院、长征职业技术学院、万向职业技术学院
线下实体店有浙大Goku出行、浙工大Goku出行、浙科院Goku出行，身份认证到浙大的同学通知到浙大Goku出行提车，身份认证到浙外、浙工大、万向职业技术学院的同学通知到浙工大Goku出行提车，身份认证到浙科院、长征职业技术学院的同学通知到浙科院Goku出行提车


"""
from playhouse.shortcuts import model_to_dict

from server.database.model import School


def add(**kwargs):
    """
    add school

    eg = {
    "name": "123456",
    "address": "bing",
    "store": "1"
    }
    既可以 store, 也可以store_id, 没有填写暂时也可以！


    :param args:
    :type args:
    :param kwargs:
    :type kwargs:
    :return: the added json
    :rtype: json
    """
    school = School.create(**kwargs)
    return model_to_dict(school)


def get(*query, **kwargs):
    school = School.get(*query, **kwargs)
    return model_to_dict(school)


def get_all():
    schools = School.select()
    new_schools = []
    for school in schools:
        new_schools.append(model_to_dict(school))
    return new_schools


def get_by_name(name):
    return model_to_dict(School.get(School.name == name))


def modify_by_name(name, modify_json):
    """

    :param school_id:
    :type school_id:
    :param modify_json:
    :type modify_json:
    :return: number of row update, 0 if not find, error if modify_json is wrong
    :rtype: int
    """
    query = School.update(**modify_json).where(School.name == name)
    return query.execute()


def remove_by_name(name):
    query = School.delete().where(School.name == name)
    return query.execute()


# ***************************** unit test ***************************** #
def add_test():
    result = add(**{"name": "", "address": "cx12"})
    print(result)


def get_test():
    result = get_by_name("2")
    print(result)


def add_template():
    template_json = [
        {
            "name": "浙江大学",
            "address": "浙江大学",
            "store": "浙大Goku出行"
        },
        {
            "name": "浙江工业大学",
            "address": "浙江工业大学",
            "store": "浙工大Goku出行"
        },
        {
            "name": "浙江科技学院",
            "address": "浙江科技学院",
            "store": "浙科院Goku出行"
        },
        {
            "name": "浙江外国语学院",
            "address": "浙江外国语学院",
            "store": "浙工大Goku出行"
        },
        {
            "name": "长征职业技术学院",
            "address": "长征职业技术学院",
            "store": "浙科院Goku出行"
        },
        {
            "name": "万向职业技术学院",
            "address": "万向职业技术学院",
            "store": "浙工大Goku出行"
        }
    ]
    for json in template_json:
        result = add(**json)
        print(result)


if __name__ == '__main__':
    pass
    print(add_template())
