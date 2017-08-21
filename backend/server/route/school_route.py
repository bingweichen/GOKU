"""

@author: Bingwei Chen

@time: 8/4/17

@desc: school route


"""

from flask import Blueprint
from flask import jsonify
# from flask import request

# from playhouse.shortcuts import model_to_dict
from server.utility.json_utility import models_to_json
from server.service import school_service

PREFIX = '/school'

school_app = Blueprint("school_app", __name__, url_prefix=PREFIX)


@school_app.route('', methods=['GET'])
def get():
    """

    :return:
    :rtype:
    """
    schools = school_service.get_all()
    return jsonify({'response': models_to_json(schools)}), 200

