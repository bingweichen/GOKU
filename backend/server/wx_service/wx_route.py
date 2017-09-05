from flask import Blueprint
from flask import request
from flask import jsonify


from server.wx_service.sign import Sign
from server.database.model import WxInfo
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
