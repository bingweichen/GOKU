import * as service from '../services/wechat';

const appId = 'wx0350234b8e970c00';
export const setWxConfig = () => {
  service.getWxConfig(location.href.split('#')[0])
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
