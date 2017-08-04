# encoding: utf-8

"""

@author:LeiJin

@file: base_model.py

@time: 7/24/17 6:50 PM

@desc:

"""
from peewee import *

database = MySQLDatabase('Goku', **{'host': '122.227.52.114', 'port': 53306, 'user': 'root',
                                    'password': '123456'})


class BaseModel(Model):
    class Meta:
        database = database

    def get_info_one(self, query):
        '''
        通用的get_info方法，获取表中的所有内容
        :param query:
        :return:
        '''
        # print( query)
        # if query!=None:
        #     try:
        return self.get(**query)
        #     except:
        #         return -1
        # else:
        #     return 0

    def get_info_several(self, offset, limit):
        '''
        分页查询多条记录
        :param amount:limit
        :param page:offset
        :return:查到的记录
        '''
        limit = int(limit)
        offset = int(offset)
        try:
            return self.select().paginate(offset, limit)
        except:
            return -1

    def add_record(self, query):
        '''
        增加一条新的记录
        :param query:
        :return:
        '''
        # try:
        # print( query)
        self.create(**query)

        #     return 1
        # except:
        #     return -1

    def delete_record(self, query):
        '''
        删除记录
        :param query:where所指向的字段
        :return:
        '''
        try:
            st = self.get(**query)
            st.delete_instance()
            return 1
        except:
            return -1
