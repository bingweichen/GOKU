# -*- coding: UTF-8 -*-
"""
@author: bingwei
@time: 8/10/17
@desc: wx_notify

通知频率为15/15/30/180/1800/1800/1800/1800/3600，单位：秒

1. 首先检查对应业务数据的状态，判断该通知是否已经处理过，如果没有处理过再进行处理，如果处理过直接返回结果成功

2. 商户系统对于支付结果通知的内容一定要做签名验证,并校验返回的订单金额是否与商户侧的订单金额一致
"""
import json
from flask import Blueprint
from flask import jsonify
from flask import request

from server.database.model import WxPayment
from server.wx.wzhifuSDK import Wxpay_server_pub
from server.service.virtual_card_service import top_up, pay_deposit
from server.service.appointment_service import appointment_payment_success

from server.database.model import User

from server.utility.constant.basic_constant import WxPaymentAttach
PREFIX = '/wx_notify'

wx_notify_app = Blueprint("wx_notify", __name__, url_prefix=PREFIX)

return_para = {
    "return_code": "SUCCESS",
    "return_msg": "OK"
}


@wx_notify_app.route('', methods=['POST'])
def wx_notify():
    data = request.get_data()

    c = Wxpay_server_pub()
    c.saveData(data)

    c.setReturnParameter("return_code", "SUCCESS")
    # 检查签名
    if c.checkSign():
        c.setReturnParameter("return_msg", "OK")
    else:
        c.setReturnParameter("return_msg", "签名失败")
        return c.returnXml()

    # 检查对应业务数据的状态，判断该通知是否已经处理过
    out_trade_no = c.data["out_trade_no"]
    wx_payment = WxPayment.get(out_trade_no=out_trade_no)
    if wx_payment.status != 'NOTPAY':
        return c.returnXml()

    # 检查金额
    total_fee = c.data["total_fee"]
    if int(wx_payment.total_fee) != int(total_fee):
        c.setReturnParameter("return_msg", "金额不一致")
        return c.returnXml()

    # 根据 attach 商家数据包 String(128) 进行支付完成操作
    attach = json.loads(c.data["attach"])
    openid = c.data["openid"]

    # 为用户进行充值
    user = User.get(we_chat_id=openid)

    if attach["code"] == WxPaymentAttach.BALANCE:
        print("top_up")
        top_up(
            card_no=user.username,
            top_up_fee=int(total_fee) / 100
        )
    if attach["code"] == WxPaymentAttach.DEPOSIT:
        print("pay_deposit")
        pay_deposit(
            card_no=user.username,
            deposit_fee=int(total_fee) / 100
        )
    if attach["code"] == WxPaymentAttach.APPOINTMENT_PRE_FEE:
        print(WxPaymentAttach.APPOINTMENT_PRE_FEE)

        appointment_payment_success(
            user=user,
            appointment_id=attach["appointment_id"]
        )



    # 更新wx_payment
    wx_payment.status = "支付完成"
    wx_payment.save()

    return c.returnXml()
