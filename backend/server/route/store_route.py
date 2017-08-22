"""

@author: Bingwei Chen

@time: 8/4/17

@desc: storage route

1. store list Add/Get/Modify

"""

from flask import Blueprint
from flask import jsonify
from flask import request

from playhouse.shortcuts import model_to_dict
from server.service import store_service
from server.utility.json_utility import models_to_json

PREFIX = '/store'

store_app = Blueprint("store", __name__, url_prefix=PREFIX)


@store_app.route('/all', methods=['GET'])
def get_stores():
    """
    eg = http://localhost:5000/store/all?username=bingwei

    :return:
    :rtype:
    """
    username = request.args.get("username")
    stores = store_service.get_all()
    if username:
        store = store_service.get_user_store(username)
        store = model_to_dict(store)
    else:
        store = {}
    return jsonify({
        'response': {
            "stores": models_to_json(stores),
            "advice_store": store
        }}), 200
