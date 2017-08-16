# -*- coding: UTF-8 -*-
"""
@author: larry.shuoren@outlook.com
@time: 8/16/17
@desc: appointment query route
"""

from flask import Blueprint
from flask import jsonify
# from flask import request

from server.service import appointment_service
from server.utility.json_utility import models_to_json

PREFIX = '/appointment_query'

appointment_query = Blueprint("appointment_query", __name__, url_prefix=PREFIX)


@appointment_query.route('/appointment_query/', methods=['GET'])
def get_appointments():
    appointments = appointment_service.get_all()
    return jsonify({
        'response': {
            "appointments": models_to_json(appointments)
        }}), 200
