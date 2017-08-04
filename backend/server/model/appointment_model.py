# encoding: utf-8

"""

@author:LeiJin

@file: appointment_model.py

@time: 7/24/17 7:13 PM

@desc:

"""
from server.model.base_model import *
from server.model.bikemodel_model import BikeModel
from server.model.user_model import *

class Appointment(BaseModel):
    date = DateTimeField()
    id = CharField(primary_key=True)
    model_id = ForeignKeyField(db_column='model_id', null=True, rel_model=BikeModel, to_field='id')
    note = CharField(null=True)
    type = CharField(null=True)
    user_id = ForeignKeyField(db_column='user_id', null=True, rel_model=User, to_field='id')
    status = CharField()

    class Meta:
        db_table = 'appointment'