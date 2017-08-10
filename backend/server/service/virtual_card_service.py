# -*- coding: UTF-8 -*-
"""
@author: larry.shuoren@outlook.com
@time: 8/10/17
@desc: virtual card service
"""

from playhouse.shortcuts import model_to_dict

from server.database.model import VirtualCard
from server.database.model import ConsumeRecord
# from server.utility.json_utility import models_to_json


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
    deposit = VirtualCard.select().where(VirtualCard.card_no == card_no)
    return model_to_dict(deposit)


def pay_deposit(card_no, deposit):
    """
    pay deposit
    :param card_no: card number
    :param deposit: deposit amount
    :return:
    """
    result = VirtualCard.update(deposit=deposit).where(VirtualCard.card_no == card_no)
    return result.execute()


def top_up(card_no, top_up_fee):
    """
    top up virtual card
    :param card_no: card number
    :param top_up_fee: top up amount
    :return:
    """
    result = VirtualCard.update(balance=VirtualCard.balance+top_up_fee).where(VirtualCard.card_no == card_no)
    return result.execute()


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
    deposit = VirtualCard.get(VirtualCard.card_no == card_no).deposit
    if deposit:
        result = VirtualCard.update(deposit=0).where(VirtualCard.card_no == card_no)
        result.execute()
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


def consume_virtual_card(card_no, amount):
    """
    consume virtual card
    :param card_no: card number
    :param amount: consume amount
    :return:
    """
    deposit = VirtualCard.get(VirtualCard.card_no == card_no).deposit
    if not deposit:
        return "No deposit"
    balance = VirtualCard.get(VirtualCard.card_no == card_no).balance
    if balance < amount:
        return "No deposit""Low Balance"
    result = VirtualCard.update(balance=VirtualCard.balance-amount).where(VirtualCard.card_no == card_no)
    result.execute()
    return "Consume succeed"


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
    # top_up("Shuo_ren", 20)
    # print(get_card_balance("Shuo_Ren"))
    # return_deposit("Shuo_Ren")
