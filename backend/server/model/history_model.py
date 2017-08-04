# encoding: utf-8

"""

@author:LeiJin

@file: history_model.py

@time: 7/24/17 7:24 PM

@desc:

"""
from datetime import *



from server.model.user_model import User
from server.model.base_model import *
from server.model.battery_model import Battery
from server.model.bikemodel_model import BikeModel
from server.model.ebike_model import Ebike



class History(BaseModel):
    battery = ForeignKeyField(db_column='battery_id', null=True, rel_model=Battery, to_field='id')
    bike_model = ForeignKeyField(db_column='bike_model_id', null=True, rel_model=BikeModel, to_field='id')
    ebike = ForeignKeyField(db_column='ebike_id', null=True, rel_model=Ebike, to_field='id')
    id = CharField(primary_key=True)
    operation = CharField()
    time = DateTimeField()
    user = ForeignKeyField(db_column='user_id', null=True, rel_model=User, to_field='id')

    class Meta:
        db_table = 'history'

# time_now=datetime.now()
# m=History()
# # print( time_now)
#
# query3={}#history
# query3['id']='286'
# query3['bike_model']='001'
# query3['user']='01'
# query3['time']=time_now
# query3['operation']='make_appointment'
# query3['battery']='001'
# query3['ebike']='001'
# # print( query3)
# m.add_record(query3)
