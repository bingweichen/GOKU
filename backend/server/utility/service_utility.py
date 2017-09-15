# encoding: utf-8

"""

@author:LeiJin

@file: service_utility.py

@time: 7/26/17 4:19 PM

@desc:

"""


def filter_number(price):
    price = ''.join([c for c in price if c in '1234567890.'])
    return price


def count_total_page(count, paginate_by):
    if count % paginate_by == 0:
        total_page = int(count / paginate_by)
    else:
        total_page = int(count / paginate_by) + 1
    return total_page


if __name__ == '__main__':
    pass
