export default function wxpay(info, callback) {
  wx.chooseWXPay({
    timestamp: info.timeStamp,
    nonceStr: info.nonceStr,
    package: info.package,
    signType: info.signType,
    paySign: info.paySign,
    success() {
      callback();
    },
  });
}
