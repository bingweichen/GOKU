# -*- coding: UTF-8 -*-
"""

@author: Bingwei Chen

@time: 8/4/17

@desc: user route

1. user register
2. user login
"""

from flask import Blueprint
from flask import jsonify
from flask import request
from flask_jwt_extended import create_access_token

from playhouse.shortcuts import model_to_dict
from peewee import DoesNotExist

from server.service import user_service
from server.utility.exception import PasswordError
from server.utility.exception import Error
PREFIX = '/user'

user_app = Blueprint("user_app", __name__, url_prefix=PREFIX)


@user_app.route('/register', methods=['POST'])
def register():
    """

    eg = {
           "username": "bingwei",
            "password": "123456",
            "name": "陈炳蔚",
            "phone": 15988731660,
            "school": "浙江大学",
            "student_id": "12358",

            "identify_number": "30032323232322"

        }

    "username": "Shuo_Ren",
            "password": "123456",
            "name": "Ren",
            "phone": 15701683747,
            "school": "浙江大学",
            "student_id": "00001",

            "identify_number": "3003232323232211"


    :return:
    :rtype:
    """
    data = request.get_json()
    username = data.pop('username')
    password = data.pop('password')

    if username is None or password is None:
        return jsonify({'response': 'invalid user or password'}), 400
    try:
        added_user = user_service.add(
            username=username,
            password=password,
            name=data.pop("name"),
            school=data.pop("school"),
            student_id=data.pop("student_id"),
            phone=data.pop("phone"),
            identify_number=data.pop("identify_number"),
            # 注释项 是可选项
            # we_chat_id=data.pop("we_chat_id"),
            # account=data.pop("account"),
            # account_type=data.pop("account_type"),
            **data)

        added_user = model_to_dict(added_user)
        added_user.pop('password')
        return jsonify({'response': added_user}), 200
    except Error:
        return jsonify({'response': {
            "message": "xxx",
            "error": Error,
        }}), 400
    except Exception as e:
        print(e)
        error = e.args[1]
        message = "字段错误"
        if "PRIMARY" in error:
            message = "用户名已存在"
        if "user_identify_number" in error:
            message = "身份证号码重复"
        if "phone" in error:
            message = "手机号码重复"
        return jsonify({'response': {
            "message": message,
            "error": error,
        }}), 400


@user_app.route('/login', methods=['POST'])
def login():
    """

    eg = {
    "username": "bingwei",
    "password": "123456"
    }

    :return:
    :rtype:
    """
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    try:
        user = user_service.login(username, password)
        user = model_to_dict(user)
        user.pop('password')

        # Identity can be any data that is json serializable
        response = {
            'response': {
                'token': create_access_token(identity=user),
                'user': user}}
        return jsonify(response), 200

    except DoesNotExist as e:
        return jsonify({
            'response': {
                "error": '%s: %s' % (str(DoesNotExist), e.args),
                "message": "用户名不存在"
            }}), 400

    except PasswordError as e:
        return jsonify({
            'response': {
                "error": '%s: %s' % (str(PasswordError), e.args),
                "message": "用户名密码错误"
            }}), 400


# 开通虚拟消费卡
@user_app.route('/virtual_card', methods=['PUT'])
def create_virtual_card():
    """

    eg = {
    "username": "Shuo_Ren"
    }

    :return:
    :rtype:
    """
    data = request.get_json()
    try:
        virtual_card = user_service.create_virtual_card(
            card_no=data.pop("username"),
            **data
        )
        return jsonify({'response': model_to_dict(virtual_card)}), 200
    except Error as e:
        return jsonify({'response': '%s: %s' % (str(Error), e.args)}), 400
