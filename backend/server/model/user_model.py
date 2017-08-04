# encoding: utf-8

"""

@author:LeiJin

@file: user_model.py

@time: 7/24/17 7:12 PM

@desc:

"""
from server.model.base_model import *
from server.model.school_model import School
from server.model.virtual_card_model import VirtualCard


class User(BaseModel):
    id = CharField(primary_key=True)
    name = CharField()
    password = CharField()
    phone = IntegerField(null=True)
    school_id = ForeignKeyField(db_column='school_id', rel_model=School, to_field='id')
    status = CharField()
    student_id = CharField(db_column='student_id')
    username = CharField(unique=True)
    vc_id = ForeignKeyField(db_column='vc_id', null=True, rel_model=VirtualCard, to_field='id')

    class Meta:
        db_table = 'user'

    def get_user_list(self, offset, limit):
        '''
        显示用户列表，for admin
        :param page: 分几页
        :param limit: 每页多少条
        :return:diclist 显示用户基本信息
        '''
        return self.select().paginate(offset, limit)

    def update_record(self, query):
        '''
        修改记录
        :param query:
        :return:
        '''
        try:
            temp = User(**query)
            temp.save()
            return 1
        except:
            return -1


#
# def delete_user(self,id):
#     '''
#     按照id删除用户
#     :param id:
#     :return:删除的条数
#     '''
#     try:
#         user = self.get(User.id == id)
#         return user.delete_instance()
#     except:
#         return -1
# def add_user(self, username, name, password, phone, status, vc_id, student_id, school_id, id):
#     try:
#         temp = User(username=username, name=name, password=password, status=status, vc_id=vc_id, student_id=student_id,
#                     id=id, school_id=school_id, phone=phone)
#         temp.save(force_insert=True)
#         return 1
#     except:
#         return -1

# m=User()
#
# add_quert = {'username': 'abd1', 'name': 'Test1', 'password': '12345', 'phone': 1235, 'status': '1',
#              'vc_id': '001', 'student_id': '012', 'school_id': '001'}
# print(m.add_record(add_quert))
# m.update_record(add_quert)

# m.add_user('c','b','123','1','001','001','07','001',915)
# g=m.get_info_several(1,10)
# print(g)
# for x in g:
#     print(x.name)

# test_user = User(username='abd1', name='Test11', password='12345')
# test_user.save()

def create_table():
    database.create_table(User)

if __name__ == "__main__":
    create_table()
