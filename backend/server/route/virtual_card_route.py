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


@virtual_card.route('/', methods=['POST'])
def pay_deposit():
    """
    pay deposit
    :return:
    """
    data = request.get_json()
    result = virtual_card_service.pay_deposit(data)
    return jsonify({'response': result}), 200


@virtual_card.route('/', methods=['POST'])
def top_up():
    """
    top up virtual card
    :return:
    """
    data = request.get_json()
    result = virtual_card_service.top_up(data)
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


@virtual_card.route('/', methods=['POST'])
def return_deposit():
    """
    return deposit
    :return:
    """
    data = request.get_json()
    result = virtual_card_service.return_deposit(data)
    return jsonify({'response': result}), 200


@virtual_card.route('/', methods=['POST'])
def consume_virtual_card():
    """
    consume virtual card
    :return:
    """
    data = request.get_json()
    result = virtual_card_service.consume_virtual_card(data)
    return jsonify({'response': result}), 200
