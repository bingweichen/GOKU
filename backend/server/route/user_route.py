# -*- coding: UTF-8 -*-
"""

@author: Bingwei Chen

@time: 8/4/17

@desc: user route

"""

from flask import Blueprint
from flask import jsonify
from flask import request

import json
from playhouse.shortcuts import model_to_dict, dict_to_model

from server.service import user_service

PREFIX = '/user'

user_app = Blueprint("user_app", __name__, url_prefix=PREFIX)


@user_app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    data.pop('username')
    data.pop('password')
    if username is None or password is None:
        return jsonify({'response': 'invalid user or password'}), 400
    try:
        added_user = user_service.add(username=username, password=password,
                                      kwargs=data)
        print("added_user", added_user)
        added_user = model_to_dict(added_user)
        print("added_user", model_to_dict(added_user))
        # added_user = json_utility.convert_to_json(added_user.to_mongo())
        added_user.pop('password')
    except Exception as e:
        return jsonify({'response': '%s: %s' % (str(Exception), e.args)}), 400
    return jsonify({'response': added_user}), 200

    # data = request.get_json()
    # username = data['username']
    # password = data['password']
    # id = data['id']
    # phone = data['phone']
    # status = data['status']
    # vc_id = data['vc_id']
    # student_id = data['student_id']
    # school_id = data['school_id']
    # name = data['name']
    # # data.pop('username')
    # # data.pop('password')
    #
    # if username is None or password is None:
    #     return jsonify({'response': 'invalid user or password'}), 400
    # try:
    #     added_user = user_basic.add_user(data)
    #     print("added_user", added_user)
    #     json_data = json.dumps(model_to_dict(added_user))
    #     print("json_data", json_data)
    #     added_user = json.dumps(str(added_user))
    #     print("added_user", added_user)
    #
    #     # added_user = json_utility.convert_to_json(added_user.to_mongo())
    #     added_user.pop('password')
    # except Exception as e:
    #     return jsonify({'response': '%s: %s' % (str(Exception), e.args)}), 400
    # return jsonify({'response': added_user}), 200


@user_app.route('/user_info', methods=['GET'])
def get_users_list():
    pass
