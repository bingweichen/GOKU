# encoding: utf-8
"""
utility used in all project

Author: BingWei Chen
Date: 2017.05.17
"""

from playhouse.shortcuts import model_to_dict


def models_to_json(models):
    new_models = []
    for model in models:
        new_models.append(model_to_dict(model))
    return new_models


def print_array(array):
    for i in array:
        print(i)
