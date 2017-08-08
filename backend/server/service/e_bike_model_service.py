"""

@author: Bingwei Chen

@time: 2017.08.07

@desc: service for e_bike_model

1. e_bike_model Add/Get/Modify/Remove

"""

from playhouse.shortcuts import model_to_dict

from server.database.model import EBikeModel


def add(**kwargs):
    """
    add e_bike_model

    eg = {
    "name": "E100小龟",
    "category": "小龟",
    "price": 2000,
    "colors": "红，蓝，绿",
    "introduction": "小龟电动车",
    }

    :param kwargs:
    :type kwargs:
    :return: the added json
    :rtype: json
    """
    e_bike_model = EBikeModel.create(**kwargs)
    return model_to_dict(e_bike_model)


def get(*query, **kwargs):
    e_bike_model = EBikeModel.get(*query, **kwargs)
    return model_to_dict(e_bike_model)


def get_all():
    e_bike_models = EBikeModel.select()
    new_e_bike_models = []
    for e_bike_model in e_bike_models:
        new_e_bike_models.append(model_to_dict(e_bike_model))
    return new_e_bike_models


def get_by_name(name):
    return model_to_dict(EBikeModel.get(EBikeModel.name == name))


def modify_by_name(name, modify_json):
    """

    :param name:
    :type name:
    :param modify_json:
    :type modify_json:
    :return: number of row update, 0 if not find, error if modify_json is wrong
    :rtype: int
    """
    query = EBikeModel.update(**modify_json).where(EBikeModel.name == name)
    return query.execute()


def remove_by_name(name):
    query = EBikeModel.delete().where(EBikeModel.name == name)
    return query.execute()


# ***************************** unit test ***************************** #
def add_template():
    template_json = [
        {
            "name": "E101小龟",
            "category": "小龟",
            "price": 2000,
            "colors": "红，蓝，绿",
            "distance": 20,
            "introduction": "小龟电动车",

        }
    ]
    for json in template_json:
        result = add(**json)
        print(result)


if __name__ == '__main__':
    pass
    print(get_all())

