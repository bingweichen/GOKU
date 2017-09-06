from urllib.request import urlopen
import json

from server.database.model import WxUser
from server.utility.exception import *

from server.wx.configure import appId, appSecret


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
