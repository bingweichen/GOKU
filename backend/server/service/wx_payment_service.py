# -*- coding: UTF-8 -*-
"""
@author: bingweiChen
@time: 20170912
@desc: virtual card service

1. 生成支付订单
"""
import uuid
from server.database.model import WxPayment

from server.wx import wx_service
# 生成商户订单
# def add(out_trade_no, total_fee):


#
def generate_payment(open_id, total_fee, body):
    # 1 生成商户订单号
    out_trade_no = uuid.uuid1()
    WxPayment.create(
        out_trade_no=out_trade_no,
        total_fee=total_fee
    )

    # 2. 发送微信预订单生成
    wx_service.get_prepay_id()

    pass
