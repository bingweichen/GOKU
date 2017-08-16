# encoding: utf-8

"""

@author:LeiJin

@file: service_utility.py

@time: 7/26/17 4:19 PM

@desc:

"""
# def check_existed(id):
#     '''
#     判断用户是否已存在
#     :param id:
#     :return:
#     '''


def filter_number(price):
    price = ''.join([c for c in price if c in '1234567890.'])
    return price

if __name__ == '__main__':

    pass