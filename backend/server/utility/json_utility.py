# encoding: utf-8
"""
utility used in all project

Author: BingWei Chen
Date: 2017.05.17
"""
import json
# import pandas as pd

from bson import ObjectId
from datetime import datetime

from playhouse.shortcuts import model_to_dict


def models_to_json(models):
    new_models = []
    for model in models:
        new_models.append(model_to_dict(model))
    return new_models


def print_array(array):
    for i in array:
        print(i)


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


def json_load(json_string):
    json_obj = json.loads(json_string)
    return json_obj


# convert bson to json
# 将ObjectId去除，用于Restful API传递
def convert_to_json(bson_obj):
    new_json_obj = JSONEncoder().encode(bson_obj)
    new_json_obj = json_load(new_json_obj)
    return new_json_obj


# # 获取ObjectId的实例内容
# def get_object(collection, object_id):
#     return mongo_manager.find_one(collection, {"_id": object_id})


# 将string转成datetime
def convert_string_to_date(timestamp):
    if isinstance(timestamp, datetime):
        return timestamp
    timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    return timestamp


# # 将json转化成DataFrame格式
# def convert_json_str_to_dataframe(arr):
#     """
#     convert input data:
#     from
#         data from staging data => database_type like, which is a list of dicts
#     to
#         DataFrame in pandas
#     """
#     col = list(arr[0].keys())
#     df_converted = pd.DataFrame([[i[j] for j in col] for i in arr],columns=col)
#     return df_converted


def me_obj_list_to_json_list(me_obj_list):
    """
    mongoengine object list to json list
    :param me_obj_list: list
    :return:
    """
    return [convert_to_json(me_obj.to_mongo()) for me_obj in
            me_obj_list]


def me_obj_list_to_dict_list(me_obj_list):
    """
    mongoengine object list to dict list
    :param me_obj_list: list
    :return:
    """
    return [me_obj.to_mongo().to_dict() for me_obj in
            me_obj_list]
