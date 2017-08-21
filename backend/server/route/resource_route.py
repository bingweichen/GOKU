# # -*- coding: UTF-8 -*-
# """
#
# @author: Bingwei Chen
#
# @time: 8/4/17
#
# @desc: resource route
#
# 1. store Add/Get/Modify/Remove
# 2. school Add/Get/Modify/Remove
#
# """
# from flask import Blueprint
# from flask import jsonify
# from flask import request
#
# from server.service import store_service
# from server.service import school_service
#
# PREFIX = '/resource'
#
# resource_app = Blueprint("resource_app", __name__, url_prefix=PREFIX)
#
#
# # ***************************** store ***************************** #
# # 代码添加 完成
# # 代码测试 完成
#
#
# # ***************************** school ***************************** #
# # 代码添加 完成
# # 代码测试 完成
#
# @resource_app.route('/school', methods=['GET'])
# @resource_app.route('/school/<string:name>',
#                     methods=['GET'])  # test complete
# def get_school(name=None):
#     if name is None:
#         print("school_id", name)
#         schools = school_service.get_all()
#     else:
#         schools = [school_service.get_by_name(name)]
#     if schools:
#         return jsonify({'response': {"schools": schools}}), 200
#     else:
#         return jsonify({'response': "no school find"}), 404
#     pass
