"""

@author: Bingwei Chen

@time: 8/4/17

@desc: 管理员
"""

from flask import Blueprint
from flask import jsonify
from flask import request

from playhouse.shortcuts import model_to_dict

from server.service import appointment_service
from server.utility.exception import Error
from server.utility.json_utility import models_to_json

PREFIX = '/manager'

manager = Blueprint("manager", __name__, url_prefix=PREFIX)


@manager.route('/appointments', methods=['GET'])
def get_appointments():
    appointments = appointment_service.get_all()
    return jsonify({
        'response': {
            "appointments": models_to_json(appointments)
        }}), 200


@manager.route('/appointment/<string:appointment_id>', methods=['GET'])
def get_appointment(appointment_id=None):
    appointment = appointment_service.get_by_id(appointment_id)
    return jsonify({
        'response': {
            "appointment": model_to_dict(appointment)}}), 200

