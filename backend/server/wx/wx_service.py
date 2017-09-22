from urllib.request import urlopen
import json
from datetime import datetime
from server.database.model import WxUser
from server.utility.exception import *

from server.wx.configure import appId, appSecret
from server.wx.wzhifuSDK import UnifiedOrder_pub, OrderQuery_pub


def get_access_token(code):
    postUrl = ("https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s"
               "&secret=%s&code=%s&grant_type=authorization_code"
               % (appId, appSecret, code))
    urlResp = urlopen(postUrl)
    urlResp = json.loads(urlResp.read())
    print("urlResp", urlResp)
    if 'errcode' in urlResp:
        raise Error("code been used")
    return urlResp


def add_or_modify_wx_user(code):
    user_info = get_access_token(code)
    open_id = user_info["openid"]
    wx_user, created = WxUser.get_or_create(open_id=open_id)
    wx_user.access_token = user_info["access_token"]
    wx_user.refresh_token = user_info["refresh_token"]
    wx_user.date = datetime.utcnow()
    wx_user.expires_in = user_info["expires_in"]
    wx_user.save()
    return open_id


def get_user_detail(open_id):
    wx_user = WxUser.get(open_id=open_id)
    access_token = wx_user.access_token
    postUrl = ("https://api.weixin.qq.com/sns/userinfo?"
               "access_token=%s&openid=%s&lang=zh_CN "
               % (access_token, open_id))
    urlResp = urlopen(postUrl)
    urlResp = json.loads(urlResp.read())
    return urlResp


# 生成微信预支付订单 返回预支付订单id, 生成带签名的json
def get_prepay_id_json(out_trade_no, body, total_fee, notify_url, openid,
                       attach):
    c = UnifiedOrder_pub()
    c.setParameter("out_trade_no", out_trade_no)
    c.setParameter("body", body)
    c.setParameter("total_fee", total_fee)
    c.setParameter("notify_url", notify_url)
    c.setParameter("trade_type", "JSAPI")
    c.setParameter("openid", openid)
    c.setParameter("attach", attach)

    # 先微信服务器获取订单
    prepay_id = c.getPrepayId()  # 不能删掉
    prepayid_json = c.getPrepayIdJson()
    return prepayid_json


# 查询订单
def order_query(out_trade_no="b084a844-9857-11e7-931a-525400"):
    c = OrderQuery_pub()
    c.setParameter("out_trade_no", out_trade_no)
    result = c.getResult()
    xml = c.arrayToXml(result)
    print("xml", xml)
    print("result", result)


if __name__ == '__main__':
    order_query()
