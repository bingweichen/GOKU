"""

@author: Bingwei Chen

@time: 8/4/17

@desc: database file

"""
from peewee import *

# database = MySQLDatabase('Zeus', charset='utf8',
#                          **{'host': '122.227.52.114', 'port': 53306,
#                             'user': 'root',
#                             'password': '123456'})

database = MySQLDatabase('Zeus', charset='utf8',
                         **{'host': '115.159.215.199', 'port': 3306,
                            'user': 'root',
                            'password': 'Chen!123'})

