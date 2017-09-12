import * as service from '../services/wechat';

const appId = 'wx79012d734b31d795';
export const setWxConfig = () => {
  service.getWxConfig(encodeURIComponent(location.href.split('#')[0]))
    .then(({ sign }) => {
      wx.config({
        timestamp: sign.timestamp,
        nonceStr: sign.nonceStr,
        signature: sign.signature,
        appId,
        debug: true,
        jsApiList: [
          'onMenuShareTimeline',
          'chooseImage',
          'scanQRCode',
          'hideAllNonBaseMenuItem',
        ],
      });
    });
};
