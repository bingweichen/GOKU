# encoding: utf-8

"""

@author:LeiJin

@file: school_model.py

@time: 7/24/17 7:11 PM

@desc:

"""
from server.model.base_model import *
from server.model.store_model import Store


class School(BaseModel):
    address = CharField(unique=True)
    id = CharField(primary_key=True)
    name = CharField(unique=True)
    store = ForeignKeyField(db_column='store_id', rel_model=Store, to_field='id')

    class Meta:
        db_table = 'school'