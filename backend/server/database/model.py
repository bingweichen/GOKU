"""

@author: Bingwei Chen

@time: 8/4/17

@desc: models

"""
from peewee import *

from server.database.db import database


class BaseModel(Model):
    class Meta:
        database = database


class Store(BaseModel):
    address = CharField(unique=True)
    id = CharField(primary_key=True)
    name = CharField(unique=True)

    class Meta:
        db_table = 'store'


class School(BaseModel):
    address = CharField(unique=True)
    id = CharField(primary_key=True)
    name = CharField(unique=True)
    store = ForeignKeyField(db_column='store_id', rel_model=Store,
                            to_field='id')

    class Meta:
        db_table = 'school'


class User(BaseModel):
    username = CharField(primary_key=True)
    password = CharField()

    name = CharField()
    phone = IntegerField(null=True)

    school = ForeignKeyField(School, related_name='users')
    status = CharField()
    student_id = CharField(db_column='student_id')

    class Meta:
        db_table = 'user'


class VirtualCard(BaseModel):
    deposit = FloatField(null=True)
    id = CharField(primary_key=True)
    security = IntegerField()

    owner = ForeignKeyField(User, related_name="virtual_cards")

    class Meta:
        db_table = 'virtual_card'


class EBikeModel(BaseModel):
    color = CharField(null=True)
    id = CharField(primary_key=True)
    introduction = CharField(null=True)
    num_sold = IntegerField()
    num_view = IntegerField()
    pics = CharField(null=True)
    price = FloatField()
    type = CharField()
    left = IntegerField()
    category = CharField()

    class Meta:
        db_table = 'bike_model'


class EBike(BaseModel):
    id = CharField(primary_key=True)
    model = ForeignKeyField(EBikeModel, related_name='e_bikes')
    state = CharField()
    user = ForeignKeyField(User, related_name='e_bikes', null=True)

    class Meta:
        db_table = 'ebike'


def create_tables():
    return database.create_tables([User, School, Store, VirtualCard,
                                   EBike, EBikeModel], safe=True)
