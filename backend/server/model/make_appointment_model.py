# encoding: utf-8

"""

@author:LeiJin

@file: make_appointment_model.py

@time: 7/24/17 7:25 PM

@desc:

"""
from server.model.appointment_model import Appointment
from server.model.base_model import *
from server.model.user_model import User


class MakeAppointment(BaseModel):
    a = ForeignKeyField(db_column='a_id', rel_model=Appointment, to_field='id')
    date = DateTimeField()
    u = ForeignKeyField(db_column='u_id', rel_model=User, to_field='id')

    class Meta:
        db_table = 'make_appointment'
        indexes = (
            (('a', 'u'), True),
        )
        primary_key = CompositeKey('a', 'u')