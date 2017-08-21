"""

@author: Bingwei Chen

@time: 8/4/17

@desc: 常量

部分可调整到数据库进行参数设置
"""
from server.service.const_service import get


# ** custom value ** #
def get_custom_const(string):
    return get(string).value


DEFAULT_APPOINTMENT_FEE = 100
DEFAULT_DEPOSIT = 199
MAXIMUM_APPOINTMENT = 5
APPOINTMENT_EXPIRED_DAYS = 7  # 7 days
BATTERY_RENT_PRICE = 1
