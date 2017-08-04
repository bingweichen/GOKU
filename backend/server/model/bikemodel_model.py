# encoding: utf-8

"""

@author:LeiJin

@file: bikemodel_model.py

@time: 7/26/17 11:08 AM

@desc:

"""
from server.model.base_model import *


class BikeModel(BaseModel):
    color = CharField(null=True)
    id = CharField(primary_key=True)
    introduction = CharField(null=True)
    num_sold = IntegerField()
    num_view = IntegerField()
    pics = CharField(null=True)
    price = FloatField()
    type = CharField()
    left =IntegerField()
    category=CharField()

    class Meta:
        db_table = 'bike_model'

    def get_bikes_by_type(self,type,amount,page,order,flag):
        '''
        获取某类ebike，并按照特定的规律排序
        :param type:
        :param amount:
        :param page:
        :param order:
        :param flag:0 正序，1 倒序
        :return:
        '''
        amount = int(amount)
        page = int(page)
        if order=='num_sold':
            order=BikeModel.num_sold
        elif order=='num_view':
            order=BikeModel.num_view
        elif order=='price':
            order=BikeModel.price
        try:
            if flag==0:
                return self.select().where(BikeModel.type==type).paginate(amount, page).order_by(order)
            else:
                return self.select().where(BikeModel.type==type).paginate(amount, page).order_by(order.desc())
        except:
            return -1

    def update_record(self,query):
        '''
        修改记录
        :param query:
        :return:
        '''
        try:
            temp = BikeModel(**query)
            temp.save()
            return 1
        except:
            return -1

