# -*- coding: UTF-8 -*-
"""
@author: larry.shuoren@outlook.com
@time: 8/10/17
@desc: virtual card route
"""

from flask import Blueprint
from flask import jsonify
from flask import request

from server.service import virtual_card_service

PREFIX = '/virtual_card'

virtual_card = Blueprint("virtual_card", __name__, url_prefix=PREFIX)


@virtual_card.route('/<string:card_no>', methods=['GET'])
def get_deposit_status(card_no):
    """
    check if the card deposited
    :param card_no: card number
    :return: True of False
    """
    deposit = virtual_card_service.get_deposit_status(card_no)
    return jsonify({'response': deposit}), 200


@virtual_card.route('/<string:card_no>/<float:deposit>', methods=['POST'])
def pay_deposit(card_no, deposit):
    """
    pay deposit
    :param card_no: card no
    :param deposit: deposit amount
    :return:
    """
    result = virtual_card_service.pay_deposit(card_no, deposit)
    return jsonify({'response': result}), 200


@virtual_card.route('/<string:card_no>/<float:top_up_fee>', methods=['POST'])
def top_up(card_no, top_up_fee):
    """
    top up virtual card
    :param card_no: card no
    :param top_up_fee: top up amount
    :return:
    """
    result = virtual_card_service.top_up(card_no, top_up_fee)
    return jsonify({'response': result}), 200


@virtual_card.route('/<string:card_no>', methods=['GET'])
def get_card_balance(card_no):
    """
    get card balance
    :param card_no: card number
    :return: balance
    """
    balance = virtual_card_service.get_card_balance(card_no)
    if balance:
        return jsonify({'response': balance}), 200
    else:
        return jsonify({'response': 'No balance found'}), 404


@virtual_card.route('/<string:card_no>', methods=['GET'])
def get_consume_record(card_no):
    """
    get consume records
    :param card_no: card number
    :return: consume records
    """
    record = virtual_card_service.get_consume_record(card_no)
    if record:
        return jsonify({'response': record}), 200
    else:
        return jsonify({'response': 'No record found'}), 404


@virtual_card.route('/<string:card_no>', methods=['POST'])
def return_deposit(card_no):
    """
    return deposit
    :param card_no: card number
    :return:
    """
    result = virtual_card_service.return_deposit(card_no)
    return jsonify({'response': result}), 200


@virtual_card.route('/<string:card_no>', methods=['POST'])
def consume_virtual_card(card_no, amount):
    """
    consume virtual card
    :param card_no: card number
    :param amount: consume amount
    :return:
    """
    result = virtual_card_service.consume_virtual_card(card_no, amount)
    return jsonify({'response': result}), 200
