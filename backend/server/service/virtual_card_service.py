# -*- coding: UTF-8 -*-
"""
@author: larry.shuoren@outlook.com
@time: 8/10/17
@desc: virtual card service
"""
from datetime import datetime

from server.database.model import VirtualCard
from server.database.model import ConsumeRecord
from server.database.model import Battery
from server.service import refund_table_service
from server.service import battery_rent_service

from server.utility.constant.custom_constant import get_custom_const
from server.utility.exception import *


# from playhouse.shortcuts import model_to_dict
# from server.utility.json_utility import models_to_json


def add(**kwargs):
    """
    add new virtual card to database
    :param kwargs: parameters to insert to database
    :return:
    """
    virtual_card = VirtualCard.create(**kwargs)
    return virtual_card


def get_deposit(card_no):
    """
    check if the card is deposited
    :param card_no: card number
    :return: True of False
    """
    # 检查电池租用情况，超过一个月冻结账户

    if not battery_rent_service.check_on_load_batter_rent_date(
            username=card_no):
        # 冻结账号
        result = freeze(card_no)
        if not result:
            print("冻结失败", card_no)
        raise Error("账号已冻结")
    virtual_card = VirtualCard.get(VirtualCard.card_no == card_no)
    return virtual_card.deposit


def pre_pay_deposit(**kwargs):
    card_no = kwargs["card_no"]

    deposit_fee = get_custom_const("DEFAULT_DEPOSIT")
    virtual_card = VirtualCard.get(VirtualCard.card_no == card_no)
    deposit = virtual_card.deposit
    if deposit >= deposit_fee:
        # 充值押金失败
        ConsumeRecord.create(
            card=card_no,
            consume_event="deposit failed",
            consume_date_time=datetime.utcnow(),
            consume_fee=deposit_fee,
            balance=virtual_card.balance)

        raise Error("无需充值押金")
    return deposit_fee


def pay_deposit(**kwargs):
    """
    pay deposit
    :param data:
        card_no: card number
        deposit_fee: deposit amount
    :return:
    """
    card_no = kwargs["card_no"]
    deposit_fee = float(kwargs["deposit_fee"])

    out_trade_no = kwargs["out_trade_no"]

    virtual_card = VirtualCard.get(VirtualCard.card_no == card_no)

    virtual_card.deposit = deposit_fee
    result = virtual_card.save()
    record = ConsumeRecord.create(
        card=card_no,
        consume_event="deposit",
        consume_date_time=datetime.utcnow(),
        consume_fee=deposit_fee,
        balance=virtual_card.balance,
        out_trade_no=out_trade_no
    )
    # 给用户虚拟卡也存一个订单号
    virtual_card = VirtualCard.get(card_no=card_no)
    virtual_card.out_trade_no = out_trade_no
    virtual_card.save()

    return result, record


def pre_top_up(**kwargs):
    """
    1. check
    :param kwargs:
    :type kwargs:
    :return:
    :rtype:
    """
    card_no = kwargs["card_no"]
    virtual_card = VirtualCard.get(VirtualCard.card_no == card_no)
    if virtual_card.deposit < get_custom_const("DEFAULT_DEPOSIT"):
        raise Error("No deposit")


def top_up(**kwargs):
    """

    2. top up virtual card
    :param data:
        card_no: card number
        top_up_fee: top up amount
    :return:
    """
    card_no = kwargs["card_no"]
    top_up_fee = float(kwargs["top_up_fee"])

    virtual_card = VirtualCard.get(VirtualCard.card_no == card_no)

    if virtual_card.deposit < get_custom_const("DEFAULT_DEPOSIT"):
        raise Error("No deposit")
    else:
        balance = virtual_card.balance + top_up_fee
        virtual_card.balance = balance
        result = virtual_card.save()
        record = ConsumeRecord.create(
            card=card_no,
            consume_event="top up",
            consume_date_time=datetime.utcnow(),
            consume_fee=top_up_fee,
            balance=balance)
        return result, record


def get_card_balance(card_no):
    """
    get card balance
    :param card_no: card number
    :return: balance
    """
    virtual_card = VirtualCard.get(VirtualCard.card_no == card_no)
    return virtual_card.balance


def return_deposit(**kwargs):
    """
    return deposit
    :param kwargs:
        card_no: card number
    :return:
    """
    card_no = kwargs["card_no"]
    # 获取支付押金订单号
    out_trade_no = VirtualCard.get(card_no=card_no).out_trade_no

    on_loan = Battery.select().where(Battery.user == card_no)
    if on_loan:
        raise Error("Battery in use")

    virtual_card = VirtualCard.get(VirtualCard.card_no == card_no)
    deposit = virtual_card.deposit
    if deposit <= 0:
        raise Error("无可退还押金")
    else:
        virtual_card.deposit = 0
        result = virtual_card.save()
        record = ConsumeRecord.create(
            card=card_no,
            consume_event="return deposit",
            consume_date_time=datetime.utcnow(),
            consume_fee=-deposit,
            balance=virtual_card.balance)
        # 记录退款
        refund_record = refund_table_service.add(
            user=kwargs["card_no"],
            out_trade_no=out_trade_no,
            type="退虚拟卡押金",
            value=deposit,
        )
        print("退虚拟卡押金" + str(deposit))
        return result, record, refund_record


def get_consume_record(card_no):
    """
    get consume record
    :param card_no: card number
    :return: consume record
    """
    record = ConsumeRecord.select().where(ConsumeRecord.card == card_no)
    return record


def consume_virtual_card(**kwargs):
    """
    consume virtual card
    :param data:
        card_no: card number
        consume_event: consume event
        amount: consume amount
    :return:
    """
    card_no = kwargs["card_no"]
    amount = float(kwargs["amount"])

    virtual_card = VirtualCard.get(VirtualCard.card_no == card_no)
    if virtual_card.deposit < get_custom_const("DEFAULT_DEPOSIT"):
        raise Error("No enough deposit")
    if virtual_card.balance <= 0:
        raise Error("Low Balance")
    balance = virtual_card.balance - amount
    # 检查用户 余额 负数冻结账户
    if balance < 0:
        virtual_card.situation = "冻结"

    virtual_card.balance = balance
    result = virtual_card.save()
    record = ConsumeRecord.create(
        card=card_no,
        consume_event="consume",
        consume_date_time=datetime.utcnow(),
        consume_fee=-amount,
        balance=balance)
    return result, record

    # deposit = get_deposit(card_no)
    # if not deposit:
    #     return "No deposit"
    # balance = get_card_balance(card_no)
    # if balance <= 0:
    #     return "Low Balance"
    # card = VirtualCard.update(balance=VirtualCard.balance-amount
    #                           ).where(VirtualCard.card_no == card_no)
    # card.execute()
    # ConsumeRecord.create(card=card_no, consume_event="consume",
    #                      consume_date_time=datetime.utcnow(),
    #                      consume_fee=-amount, balance=balance-amount)
    # return "Consume " + str(amount) + " succeed"


def get_virtual_card(card_no):
    """
    get virtual card information
    :param card_no: card number
    :return: card number, deposit and balance
    """
    virtual_card = VirtualCard.get(VirtualCard.card_no == card_no)
    return virtual_card


def check_deposit(username):
    """
    check if the card has enough deposit
    :param username: card holder
    :return: True or raise an error
    """
    virtual_card = VirtualCard.get(VirtualCard.card_no == username)
    if virtual_card:
        deposit = virtual_card.deposit
        if deposit >= get_custom_const("DEFAULT_DEPOSIT"):
            return True
        else:
            raise Error("没有足够的押金")
    else:
        raise Error("未开通虚拟卡")


def check_status(username):
    """
    检查账户状态是否异常

    :param username:
    :type username:
    :return:
    :rtype:
    """
    virtual_card = VirtualCard.get(VirtualCard.card_no == username)
    if virtual_card.balance < 0:
        raise Error("余额不足")
    if virtual_card.situation != "正常":
        raise Error("账户异常")
    return True


def check_value(card_no):
    """
    check if the card can be used
    :param card_no: card number of user
    :return: True if usable or raise an error
    """
    virtual_card = VirtualCard.get(VirtualCard.card_no == card_no)
    if virtual_card.deposit < get_custom_const("DEFAULT_DEPOSIT"):
        raise Error("No enough deposit")
    if virtual_card.balance <= 0:
        raise Error("No Balance")
    return True


# 冻结账号
def freeze(card_no):
    virtual_card = VirtualCard.get(card_no=card_no)
    virtual_card.situation = "冻结"
    return virtual_card.save()


# 解冻账号
def re_freeze(card_no):
    virtual_card = VirtualCard.get(card_no=card_no)
    virtual_card.situation = "正常"
    return virtual_card.save()


# def normal(card_no):
#     virtual_card = VirtualCard.get(card_no=card_no)
#     virtual_card.situation = "正常"
#     return virtual_card.save()


# ***************************** for test ***************************** #
def add_template():
    template_json = [
        {
            "card_no": "Shuo_Ren"
        }
    ]
    for json in template_json:
        result = add(**json)
        print(result)


if __name__ == '__main__':
    pass
    return_deposit(card_no="bingwei", username="bingwei",
                   account="123456", account_type="weChat")
