# -*- coding: UTF-8 -*-
"""
@author: larry.shuoren@outlook.com
@time: 8/10/17
@desc: virtual card service
"""
from datetime import datetime

from playhouse.shortcuts import model_to_dict

from server.database.model import VirtualCard
from server.database.model import ConsumeRecord
from server.database.model import Battery
from server.service import refund_table_service

from server.utility.constant import DEFAULT_DEPOSIT
from server.utility.json_utility import models_to_json

from server.utility.exception import *


def add(**kwargs):
    """
    add new virtual card to database
    :param kwargs: parameters to insert to database
    :return:
    """
    virtual_card = VirtualCard.create(**kwargs)
    return virtual_card


def get_deposit_status(card_no):
    """
    check if the card is deposited
    :param card_no: card number
    :return: True of False
    """
    deposit = VirtualCard.get(VirtualCard.card_no == card_no)
    if deposit:
        deposit = model_to_dict(deposit)
        return float(deposit["deposit"])
    else:
        return "No deposit found"


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
    deposit = get_deposit_status(card_no)
    balance = get_card_balance(card_no)
    if deposit < DEFAULT_DEPOSIT:
        result = VirtualCard.update(deposit=deposit_fee
                                    ).where(VirtualCard.card_no == card_no)
        result.execute()
        ConsumeRecord.create(card=card_no, consume_event="deposit",
                             consume_date_time=datetime.now(),
                             consume_fee=deposit_fee, balance=balance)
        return "Deposit succeed"
    else:
        return "You need not pay deposit"


def top_up(**kwargs):
    """
    top up virtual card
    :param data:
        card_no: card number
        top_up_fee: top up amount
    :return:
    """
    card_no = kwargs["card_no"]
    top_up_fee = float(kwargs["top_up_fee"])
    deposit = get_deposit_status(card_no)
    if not deposit:
        return "No deposit"
    result = VirtualCard.update(balance=VirtualCard.balance+top_up_fee
                                ).where(VirtualCard.card_no == card_no)
    balance = get_card_balance(card_no)
    result.execute()
    ConsumeRecord.create(card=card_no, consume_event="top up",
                         consume_date_time=datetime.now(),
                         consume_fee=top_up_fee,
                         balance=balance+top_up_fee)
    return "Top up succeed"


def get_card_balance(card_no):
    """
    get card balance
    :param card_no: card number
    :return: balance
    """
    balance = VirtualCard.get(VirtualCard.card_no == card_no)
    return balance.balance


def return_deposit(**kwargs):
    """
    return deposit
    :param kwargs:
        card_no: card number
    :return:
    """
    card_no = kwargs["card_no"]
    deposit = get_deposit_status(card_no)
    balance = get_card_balance(card_no)
    on_loan = Battery.select().where(Battery.user == card_no)
    if on_loan:
        raise Error("Battery in use")
    if deposit:
        result = VirtualCard.update(deposit=0
                                    ).where(VirtualCard.card_no == card_no)
        result.execute()
        ConsumeRecord.create(card=card_no, consume_event="return deposit",
                             consume_date_time=datetime.now(),
                             consume_fee=-deposit, balance=balance)
        # 记录退款
        refund_table_service.add(
            user=kwargs["username"],
            account=kwargs["account"],
            account_type=kwargs["account_type"],
            type="退虚拟卡押金",
            value=deposit,
            comment=kwargs.get("comment")
        )
        print("退虚拟卡押金" + str(deposit))
        return "Return deposit succeed"
    else:
        return "No deposit refundable"


def get_consume_record(card_no):
    """
    get consume record
    :param card_no: card number
    :return: consume record
    """
    record = ConsumeRecord.select().where(ConsumeRecord.card == card_no)
    return models_to_json(record)


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

    deposit = get_deposit_status(card_no)
    if not deposit:
        return "No deposit"
    balance = get_card_balance(card_no)
    if balance <= 0:
        return "Low Balance"
    card = VirtualCard.update(balance=VirtualCard.balance-amount
                              ).where(VirtualCard.card_no == card_no)
    card.execute()
    ConsumeRecord.create(card=card_no, consume_event="consume",
                         consume_date_time=datetime.now(),
                         consume_fee=-amount, balance=balance-amount)
    return "Consume " + str(amount) + " succeed"


def get_virtual_card_info(card_no):
    """
    get virtual card information
    :param card_no: card number
    :return: card number, deposit and balance
    """
    virtual_card = VirtualCard.get(VirtualCard.card_no == card_no)
    info = model_to_dict(virtual_card)
    return {"card no": info["card_no"]["username"],
            "deposit": info["deposit"],
            "balance": info["balance"]}


def check_deposit(username):
    """
    check if the card has enough deposit
    :param username: card holder
    :return: True or raise an error
    """
    virtual_card = VirtualCard.get(VirtualCard.card_no == username)
    if virtual_card:
        deposit = virtual_card.deposit
        if deposit >= DEFAULT_DEPOSIT:
            return True
        else:
            raise Error("no enough deposit")
    else:
        raise Error("no virtual card")


def check_value(card_no):
    """
    check if the card can be used
    :param card_no: card number of user
    :return: True if usable or raise an error
    """
    virtual_card = VirtualCard.get(VirtualCard.card_no == card_no)
    if virtual_card.deposit < DEFAULT_DEPOSIT:
        raise Error("No enough deposit")
    if virtual_card.balance <= 0:
        raise Error("No Balance")
    return True


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
    print("hello world!")
    # add_template()
    # print(pay_deposit("Shuo_Ren", 199))
    # print(get_deposit_status("Shuo_Ren"))
    # print(top_up("Shuo_Ren", 200))
    # print(get_card_balance("Shuo_Ren"))
    # return_deposit("Shuo_Ren")
    # print(consume_virtual_card("Shuo_Ren", "任性", 10000))
    # print(consume_virtual_card("Shuo_Ren", "不任性", 10))
    # print(get_virtual_card_info("Shuo_Ren"))
    # print(get_consume_record("Shuo_Ren"))
    return_deposit(card_no="bingwei", username="bingwei",
                   account="123456", account_type="weChat")
