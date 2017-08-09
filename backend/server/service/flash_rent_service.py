# -*- coding: UTF-8 -*-
"""
@author: Shuo Ren
@time: 8.9.2017
@desc: service for flash rent
"""

from playhouse.shortcuts import model_to_dict
from server.database.model import EBike


def get_e_bike_list():
    e_bikes = EBike.select()
    return model_to_dict(e_bikes)

