# encoding: utf-8

"""

@author:LeiJin

@file: coupon_user.py

@time: 7/24/17 7:26 PM

@desc:

"""

from server.model.base_model import *
from server.model.coupon_model import Coupon
from server.model.user_model import User


class UserCoupon(BaseModel):
    coupon = ForeignKeyField(db_column='coupon_id', rel_model=Coupon, to_field='id')
    date = DateTimeField()
    user = ForeignKeyField(db_column='user_id', rel_model=User, to_field='id')

    class Meta:
        db_table = 'user_coupon'
        indexes = (
            (('user', 'coupon'), True),
        )
        primary_key = CompositeKey('coupon', 'user')