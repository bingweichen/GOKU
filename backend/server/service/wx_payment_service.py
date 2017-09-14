# -*- coding: UTF-8 -*-
"""
@author: bingweiChen
@time: 20170912
@desc: virtual card service

1. 生成支付订单
"""
import json
import uuid
from server.database.model import WxPayment

from server.wx import wx_service
from server.utility.constant.basic_constant import BasicConstant


# 储存商户订单，返回prepay_id
def get_prepay_id_json(openid, total_fee, body, attach, appointment_id=None):
    total_fee = int(total_fee)

    # 1 生成商户订单号
    out_trade_no = str(uuid.uuid1())[:30]
    # 储存商户订单
    WxPayment.create(
        out_trade_no=out_trade_no,
        total_fee=total_fee,
        appointment=appointment_id,
        openid=openid,
        attach=attach
    )

    # 2. 发送微信预订单生成
    attach = json.dumps(attach)

    notify_url = BasicConstant.notify_url
    prepay_id_json = wx_service.get_prepay_id_json(
        out_trade_no=out_trade_no,
        body=body,
        total_fee=total_fee,
        notify_url=notify_url,
        openid=openid,
        attach=attach
    )
    return prepay_id_json


if __name__ == '__main__':
    # pass
    # get_prepay_id_json(
    #     openid="11", total_fee=1, body="1", attach, appointment_id=None
    # )
    WxPayment.create(
        out_trade_no="11",
        total_fee="111",
        appointment=7,
        openid="11",
        attach="11"
    )
