# """
#
# @author: Bingwei Chen
#
# @time: 2017.08.07
#
# @desc: service for e_bike
#
# 1. e_bike Add/Get/Modify/Remove
#
# 未完成
# """
#
# from playhouse.shortcuts import model_to_dict
#
# from server.database.model import EBike
#
#
# def add(**kwargs):
#     """
#     add e_bike
#
#     eg = {
#     "name": "E100小龟",
#     "category": "小龟",
#     "price": 2000,
#     "colors": "红，蓝，绿",
#     "introduction": "小龟电动车",
#     }
#
#     :param kwargs:
#     :type kwargs:
#     :return: the added json
#     :rtype: json
#     """
#     e_bike = EBike.create(**kwargs)
#     return model_to_dict(e_bike)
#
#
# def get(*query, **kwargs):
#     e_bike = EBike.get(*query, **kwargs)
#     return model_to_dict(e_bike)
#
#
# def get_all():
#     e_bikes = EBike.select()
#     new_e_bikes = []
#     for e_bike in e_bikes:
#         new_e_bikes.append(model_to_dict(e_bike))
#     return new_e_bikes
#
#
# def get_by_name(name):
#     return model_to_dict(EBike.get(EBike.name == name))
#
#
# def modify_by_name(name, modify_json):
#     """
#
#     :param name:
#     :type name:
#     :param modify_json:
#     :type modify_json:
#     :return: number of row update, 0 if not find, error if modify_json is wrong
#     :rtype: int
#     """
#     query = EBike.update(**modify_json).where(EBike.name == name)
#     return query.execute()
#
#
# def remove_by_name(name):
#     query = EBike.delete().where(EBike.name == name)
#     return query.execute()
#
#
# # ***************************** unit test ***************************** #
# def add_template():
#     template_json = [
#         {
#             "name": "E101小龟",
#             "category": "小龟",
#             "price": 2000,
#             "colors": "红，蓝，绿",
#             "distance": 20,
#             "introduction": "小龟电动车",
#
#         }
#     ]
#     for json in template_json:
#         result = add(**json)
#         print(result)
#
#
# if __name__ == '__main__':
#     pass
#     print(get_all())
#
