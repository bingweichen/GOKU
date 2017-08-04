# encoding: utf-8

"""

@author:LeiJin

@file: virtual_card_model.py

@time: 7/24/17 7:12 PM

@desc:

"""
from server.model.base_model import *
class VirtualCard(BaseModel):
    deposit = FloatField(null=True)
    id = CharField(primary_key=True)
    security = IntegerField()

    class Meta:
        db_table = 'virtual_card'