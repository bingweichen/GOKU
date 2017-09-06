from urllib.request import urlopen
import time
import json

from server.database.model import WxInfo


class Basic:
    def __init__(self):
        self.__accessToken = ''
        self.__leftTime = 0
        self.__jsapi_ticket = ''
        self.__leftTime_ticket = 0

    def __real_get_access_token(self):
        appId = "wx0350234b8e970c00"
        appSecret = "97dfd4483fd75d568da28d3ea9508632"

        # 获取 access_token
        postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type="
                   "client_credential&appid=%s&secret=%s" % (appId, appSecret))
        urlResp = urlopen(postUrl)
        urlResp = json.loads(urlResp.read())
        self.__accessToken = urlResp['access_token']
        self.__leftTime = urlResp['expires_in']

        # 获取 jsapi_ticket
        postUrl_1 = ("https://api.weixin.qq.com/cgi-bin/ticket/getticket?"
                     "access_token=%s&type=jsapi" % self.__accessToken)
        urlResp_1 = urlopen(postUrl_1)
        urlResp_1 = json.loads(urlResp_1.read())
        self.__jsapi_ticket = urlResp_1['ticket']
        self.__leftTime_ticket = urlResp_1['expires_in']

        accessToken = WxInfo.get(key='accessToken')
        accessToken.value = self.__accessToken
        accessToken.save()
        jsapi_ticket = WxInfo.get(key='jsapi_ticket')
        jsapi_ticket.value = self.__jsapi_ticket
        jsapi_ticket.save()

        print(self.__accessToken)
        print(self.__leftTime)
        print(self.__jsapi_ticket)
        print(self.__leftTime_ticket)

    def get_access_token(self):
        if self.__leftTime < 100:
            self.__real_get_access_token()
        return self.__accessToken

    def run(self):
        while (True):
            if self.__leftTime > 100:
                time.sleep(2)
                self.__leftTime -= 2
            else:
                self.__real_get_access_token()


if __name__ == '__main__':
    basic = Basic()
    basic.run()
