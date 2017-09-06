from flask import Blueprint
from flask import request
from flask import jsonify

from server.wx import wx_service
from server.wx.sign import Sign
from server.database.model import WxInfo
from server.utility.exception import *

PREFIX = '/wx'

wx_app = Blueprint("wx_app", __name__, url_prefix=PREFIX)


@wx_app.route('/get_sign', methods=['GET'])
def get_sign():
    url = request.args.get("url")
    jsapi_ticket = WxInfo.get(key='jsapi_ticket').value
    sign = Sign(jsapi_ticket, url)
    sign.sign()

    return jsonify({
        'response': {
            "sign": sign.ret
        }}), 200


@wx_app.route('/code_to_openid', methods=['POST'])
# using code to change Wxuser and return openid
def code_to_openid():
    code = request.args.get("code")
    try:
        open_id = wx_service.add_or_modify_wx_user(code=code)
        return jsonify({
            'response': {
                "open_id": open_id
            }}), 200

    except Error as e:
        return jsonify({
            'response': {
                "error": e.args
            }}), 400



