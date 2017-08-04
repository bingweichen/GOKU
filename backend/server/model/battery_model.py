# encoding: utf-8

"""

@author:LeiJin

@file: battery_model.py

@time: 7/24/17 7:14 PM

@desc:

"""
from server.model.base_model import *

class Battery(BaseModel):
    date = DateTimeField()
    id = CharField(primary_key=True)
    status = CharField()

    class Meta:
        db_table = 'battery'