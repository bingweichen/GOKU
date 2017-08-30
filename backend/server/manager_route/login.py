# from flask import Blueprint
# from flask import jsonify
# from flask import request
#
# from playhouse.shortcuts import model_to_dict
# from server.utility.json_utility import models_to_json
#
# from server.service import user_service
# from server.service import appointment_service
# from server.service import refund_table_service
# from server.service import report_table_service
# from server.service import virtual_card_service
# from server.service import battery_record_service
# from server.service import battery_rent_service
#
# from server.utility.exception import Error
#
# PREFIX = '/manager/user'
#
# user_app = Blueprint("user_setting", __name__, url_prefix=PREFIX)
#
#
# @user_app.route('/login', methods=['POST'])
# def login():
#     """
#
#     eg = {
#     "username": "bingwei",
#     "password": "123456"
#     }
#
#     :return:
#     :rtype:
#     """
#     username = request.json.get('username', None)
#     password = request.json.get('password', None)
#     try:
#         user = user_service.login(username, password)
#         user = model_to_dict(user)
#         user.pop('password')
#
#         # Identity can be any data that is json serializable
#         response = {
#             'response': {
#                 'token': create_access_token(identity=user),
#                 'user': user}}
#         return jsonify(response), 200
#
#     except DoesNotExist as e:
#         return jsonify({
#             'response': {
#                 "error": '%s: %s' % (str(DoesNotExist), e.args),
#                 "message": "用户名不存在"
#             }}), 400
#
#     except PasswordError as e:
#         return jsonify({
#             'response': {
#                 "error": '%s: %s' % (str(PasswordError), e.args),
#                 "message": "用户名密码错误"
#             }}), 400