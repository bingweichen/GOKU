from urllib.request import urlopen
import json

from server.database.model import WxUser
from server.utility.exception import *

from server.wx.configure import appId, appSecret
from server.wx.wzhifuSDK import UnifiedOrder_pub, \
    Common_util_pub, OrderQuery_pub


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
def get_prepay_id_json(out_trade_no, body, total_fee, notify_url, openid, attach):

    c = UnifiedOrder_pub()
    c.setParameter("out_trade_no", out_trade_no)
    c.setParameter("body", body)
    c.setParameter("total_fee", total_fee)
    c.setParameter("notify_url", notify_url)
    c.setParameter("trade_type", "JSAPI")
    c.setParameter("openid", openid)
    c.setParameter("attach", attach)

    # 先微信服务器获取订单
    prepay_id = c.getPrepayId()
    prepayid_json = c.getPrepayIdJson()
    # xml = c.array_to_xml(prepayid_json)
    # print("xml", xml)
    return prepayid_json


# 查询订单
def order_query(out_trade_no="b084a844-9857-11e7-931a-525400"):
    c = OrderQuery_pub()
    c.setParameter("out_trade_no", out_trade_no)
    result = c.getResult()
    xml = c.arrayToXml(result)
    print("xml", xml)
    print("result", result)


# 通过预支付订单, 生成带签名的
# def prepay_id_to_package_json(prepay_id):




# import hashlib
# from urllib.parse import quote

# def wx_pay_sign():
#
#     temp = {
#         "appid": "wxd930ea5d5a258f4f",
#         "mch_id": "10000100",
#         "device_info": "1000",
#         "body": "test",
#         "nonce_str": "ibuaiVcKdpRxkhJA"
#     }
#     stringA = ""
#     for key, value in temp.items():
#         stringA += '%s=%s&' % (key, value)
#     stringA = stringA[:-1]
#     print(stringA)
#     stringSignTemp = stringA + "&key=192006250b4c09247ec02edce69f6a2d"
#     print("stringSignTemp", stringSignTemp)
#
#     m = hashlib.md5()
#     m.update(stringSignTemp.encode('utf-8'))
#     sign = m.hexdigest().upper()
#     # sign = sign.toUpperCase()
#     # sign = hashlib.sha256(stringSignTemp.encode('utf-8')).hexdigest().upper()
#     # sign=MD5(stringSignTemp).toUpperCase()
#
#     print(sign)

# def getSign(obj):
#     """生成签名"""
#     # 签名步骤一：按字典序排序参数,formatBizQueryParaMap已做
#     String = formatBizQueryParaMap(obj, False)
#     # 签名步骤二：在string后加入KEY
#     String = "{0}&key={1}".format(String, "192006250b4c09247ec02edce69f6a2d")
#     # 签名步骤三：MD5加密
#     String = hashlib.md5(String.encode('utf-8')).hexdigest()
#     # 签名步骤四：所有字符转为大写
#     result_ = String.upper()
#     return result_
#
#
# def formatBizQueryParaMap(paraMap, urlencode):
#     """格式化参数，签名过程需要使用"""
#     slist = sorted(paraMap)
#     buff = []
#     for k in slist:
#         v = quote(paraMap[k]) if urlencode else paraMap[k]
#         buff.append("{0}={1}".format(k, v))
#
#     return "&".join(buff)

if __name__ == '__main__':
    order_query()
    # temp = {
    #     "appid": "wxd930ea5d5a258f4f",
    #     "mch_id": "10000100",
    #     "device_info": "1000",
    #     "body": "test",
    #     "nonce_str": "ibuaiVcKdpRxkhJA"
    # }
    # result = getSign(temp)
    # print("result", result)
