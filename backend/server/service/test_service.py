# """
# 中文
# """
# from server.database.model import *
# from playhouse.shortcuts import model_to_dict
#
#
# def add(**kwargs):
#     """
#     add store
#
#     eg = {
#     "name": "123456",
#     "address": "bing"
#     }
#
#     :param kwargs:
#     :type kwargs:
#     :return: the added json
#     :rtype: json
#     """
#     store = Store.create(**kwargs)
#     return model_to_dict(store)
#
#
# # ***************************** unit test ***************************** #
# def add_template():
#     my_test_json = ["a", "b"]
#     result = Test.create(array=my_test_json)
#     print(model_to_dict(result))
#     # template_json = [
#     #     {
#     #         "array": ["a", "b"],
#     #     }
#     #
#     # ]
#     # for json in template_json:
#     #     result = add(**json)
#     #     print(result)
#
#
# def get():
#     result = Test.get(id=2)
#     print(result.array[0])
#
# if __name__ == '__main__':
#     pass
#     get()
