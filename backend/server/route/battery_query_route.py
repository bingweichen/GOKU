# -*- coding: UTF-8 -*-
"""
@author: larry.shuoren@outlook.com
@time: 8/10/17
@desc: virtual card route
"""

from flask import Blueprint
from flask import jsonify
from flask import request

from server.service import battery_rent_service

PREFIX = '/battery_query'

battery_query = Blueprint("battery_query", __name__, url_prefix=PREFIX)


@battery_query.route('/total_use', methods=['GET'])
def get_total_uses_amount():
    battery_rent_service.manager_get_total_uses_amount()
    pass


@battery_query.route('/current_use', methods=['GET'])
def get_current_uses_amount():
    battery_rent_service.manager_get_current_uses_amount()
    pass


@battery_query.route('/use_status/<string:serial_number>', methods=['GET'])
def get_use_status_by_id(serial_number):
    battery_rent_service.manager_get_use_status_by_id(serial_number)
    pass


@battery_query.route('/history_record/<string:serial_number>/<int:days>',
                     methods=['GET'])
def get_history_record_by_id(serial_number, days):
    battery_rent_service.manager_get_history_record_by_id(serial_number, days)
    pass
