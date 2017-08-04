"""

@author: Bingwei Chen

@time: 8/4/17

@desc: database file

"""
from peewee import *

database = MySQLDatabase('Zeus', **{'host': '122.227.52.114', 'port': 53306,
                                    'user': 'root',
                                    'password': '123456'})
