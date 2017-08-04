# encoding: utf-8

"""

@author:LeiJin

@file: customer_service_model.py

@time: 7/24/17 7:16 PM

@desc:

"""
from server.model.base_model import *
class CustomerService(BaseModel):
    email = CharField(null=True)
    id = CharField(primary_key=True)
    name = CharField()
    phone = IntegerField(null=True)
    wechat = CharField(db_column='wechat_id', null=True)

    class Meta:
        db_table = 'customer_service'