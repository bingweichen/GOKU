# -*- coding: UTF-8 -*-

"""
@author: bingweiChen
@time: 8/9/17
@desc: e-bike rent service
"""
from server.database.model import Logs


def get_all():
    logs = Logs.select()
    return logs
