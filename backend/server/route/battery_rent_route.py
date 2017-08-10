# -*- coding: UTF-8 -*-
"""
@author: larry.shuoren@outlook.com
@time: 8/10/17
@desc: battery rent route
"""

from flask import Blueprint
from flask import jsonify
from flask import request

from server.service import battery_rent_service

PREFIX = '/battery_rent'

battery_rent = Blueprint("battery_rent", __name__, url_prefix=PREFIX)


@battery_rent.route('/<string:b_id>', methods=['GET'])
def get_battery_rent_info(b_id):
    info = battery_rent_service.get_battery_rent_info(b_id)
    if info:
        return jsonify({'response': info}), 200
    else:
        return jsonify({'response': 'No information found'}), 404


@battery_rent.route('/', methods=['GET'])
def get_deposit_status():
    pass


@battery_rent.route('/', methods=['POST'])
def modify_use_status():
    pass


@battery_rent.route('/', methods=['PUT'])
def add_repair_report():
    pass


@battery_rent.route('/', methods=['POST'])
def pay_deposit():
    pass


@battery_rent.route('/', methods=['POST'])
def top_up():
    pass


@battery_rent.route('/', methods=['GET'])
def get_card_balance():
    pass


@battery_rent.route('/', methods=['GET'])
def get_consume_record():
    pass


@battery_rent.route('/', methods=['POST'])
def return_deposit():
    pass


@battery_rent.route('/', methods=['PUT'])
def add_battery():
    pass
