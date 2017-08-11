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
# from server.utility.json_utility import models_to_json

DEFAULT_DEPOSIT = 199.0


def add(**kwargs):
    """
    add new virtual card to database
    :param kwargs: parameters to insert to database
    :return:
    """
    virtual_card = VirtualCard.create(**kwargs)
    return model_to_dict(virtual_card)


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


def pay_deposit(card_no, deposit_fee):
    """
    pay deposit
    :param card_no: card number
    :param deposit_fee: deposit amount
    :return:
    """
    deposit = get_deposit_status(card_no)
    balance = get_card_balance(card_no)
    if deposit < DEFAULT_DEPOSIT:
        result = VirtualCard.update(deposit=deposit_fee).where(VirtualCard.card_no == card_no)
        result.execute()
        ConsumeRecord.create(card=card_no, consume_event="deposit",
                             consume_date_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                             consume_fee=deposit_fee, balance=balance)
        return "Deposit succeed"
    else:
        return "You need not pay deposit"


def top_up(card_no, top_up_fee):
    """
    top up virtual card
    :param card_no: card number
    :param top_up_fee: top up amount
    :return:
    """
    deposit = get_deposit_status(card_no)
    if not deposit:
        return "No deposit"
    result = VirtualCard.update(balance=VirtualCard.balance+top_up_fee).where(VirtualCard.card_no == card_no)
    balance = get_card_balance(card_no)
    result.execute()
    ConsumeRecord.create(card=card_no, consume_event="top up",
                         consume_date_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                         consume_fee=top_up_fee, balance=balance+top_up_fee)
    return "Top up succeed"


def get_card_balance(card_no):
    """
    get card balance
    :param card_no: card number
    :return: balance
    """
    balance = VirtualCard.get(VirtualCard.card_no == card_no)
    return balance.balance


def return_deposit(card_no):
    """
    return deposit
    :param card_no: card number
    :return:
    """
    deposit = get_deposit_status(card_no)
    balance = get_card_balance(card_no)
    if deposit:
        result = VirtualCard.update(deposit=0).where(VirtualCard.card_no == card_no)
        result.execute()
        ConsumeRecord.create(card=card_no, consume_event="return deposit",
                             consume_date_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                             consume_fee=-deposit, balance=balance)
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
    return model_to_dict(record)


def consume_virtual_card(card_no, consume_event, amount):
    """
    consume virtual card
    :param card_no: card number
    :param consume_event: consume event
    :param amount: consume amount
    :return:
    """
    deposit = get_deposit_status(card_no)
    if not deposit:
        return "No deposit"
    balance = get_card_balance(card_no)
    if balance < amount:
        return "Low Balance"
    card = VirtualCard.update(balance=VirtualCard.balance-amount).where(VirtualCard.card_no == card_no)
    card.execute()
    ConsumeRecord.create(card=card_no, consume_event=consume_event,
                         consume_date_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                         consume_fee=-amount, balance=balance-amount)
    return "Consume " + str(amount) + " succeed"


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
    print(top_up("Shuo_Ren", 200))
    # print(get_card_balance("Shuo_Ren"))
    # return_deposit("Shuo_Ren")
    # print(consume_virtual_card("Shuo_Ren", "任性", 10000))
    # print(consume_virtual_card("Shuo_Ren", "不任性", 10))
