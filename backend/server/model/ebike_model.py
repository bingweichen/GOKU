# encoding: utf-8

"""

@author:LeiJin

@file: ebike_model.py

@time: 7/24/17 7:23 PM

@desc:

"""
from server.model.user_model import User
from server.model.base_model import *
from server.model.bikemodel_model import BikeModel


class Ebike(BaseModel):
    id = CharField(primary_key=True)
    model_id = ForeignKeyField(db_column='model_id', rel_model=BikeModel, to_field='id')
    state = CharField()
    user_id = ForeignKeyField(db_column='user_id', null=True, rel_model=User, to_field='id')

    class Meta:
        db_table = 'ebike'