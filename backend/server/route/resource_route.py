# -*- coding: UTF-8 -*-
"""

@author: Bingwei Chen

@time: 8/4/17

@desc: resource route

1. store Add/Get/Modify/Remove
1. school Add/Get/Modify/Remove
2. e_bike Add/Get/Modify/Remove

"""
from flask import Blueprint
from flask import jsonify
from flask import request

from server.service import store_service
from server.service import school_service

PREFIX = '/resource'

resource_app = Blueprint("resource_app", __name__, url_prefix=PREFIX)


# ***************************** store ***************************** #
# 代码添加 完成
# 代码测试 完成
@resource_app.route('/store', methods=['PUT'])  # test complete
def add_store():
    data = request.get_json()
    store = store_service.add(**data)
    if store:
        return jsonify({'response': store}), 200
    pass


@resource_app.route('/store', methods=['GET'])
@resource_app.route('/store/<string:name>',
                    methods=['GET'])  # test complete
def get_store(name=None):
    if name is None:
        stores = store_service.get_all()
    else:
        stores = [store_service.get_by_name(name)]
    if stores:
        return jsonify({'response': {"stores": stores}}), 200
    else:
        return jsonify({'response': "no store find"}), 404
    pass


@resource_app.route('/store/<string:name>',
                    methods=['POST'])  # test complete
def modify_store(name):
    data = request.get_json()
    modify_json = data
    result = store_service.modify_by_name(name, modify_json)
    if result:
        return jsonify({'response': "modify success"}), 200
    else:
        return jsonify({'response': "no store find"}), 404
    pass


@resource_app.route('/store/<string:name>',
                    methods=['DELETE'])  # test complete
def remove_store(name):
    result = store_service.remove_by_name(name)
    if result:
        return jsonify({'response': "delete success"}), 200
    else:
        return jsonify({'response': "no store find"}), 404
    pass


# ***************************** school ***************************** #
# 代码添加 完成
# 代码测试 完成
@resource_app.route('/school', methods=['PUT'])
def add_school():
    data = request.get_json()
    school = school_service.add(**data)
    if school:
        return jsonify({'response': school}), 200
    pass


@resource_app.route('/school', methods=['GET'])
@resource_app.route('/school/<string:name>',
                    methods=['GET'])  # test complete
def get_school(name=None):
    if name is None:
        print("school_id", name)
        schools = school_service.get_all()
    else:
        schools = [school_service.get_by_name(name)]
    if schools:
        return jsonify({'response': {"schools": schools}}), 200
    else:
        return jsonify({'response': "no school find"}), 404
    pass


@resource_app.route('/school/<string:name>',
                    methods=['POST'])  # test complete
def modify_school(name):
    data = request.get_json()
    modify_json = data
    result = school_service.modify_by_name(name, modify_json)
    if result:
        return jsonify({'response': "modify success"}), 200
    else:
        return jsonify({'response': "no school find"}), 404
    pass


@resource_app.route('/school/<string:name>',
                    methods=['DELETE'])  # test complete
def remove_school(name):
    result = school_service.remove_by_name(name)
    if result:
        return jsonify({'response': "delete success"}), 200
    else:
        return jsonify({'response': "no school find"}), 404
    pass
