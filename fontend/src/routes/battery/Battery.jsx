import React, { Component } from 'react';
import { NoticeBar, Icon, Modal, ActivityIndicator, Toast, Button } from 'antd-mobile';
import moment from 'moment';
import { connect } from 'dva';
import { hashHistory } from 'dva/router';
import { getVirtualCard, openVirtualCardService, batteryReport } from '../../services/battery.js';
import styles from './index.less';

const { alert, prompt } = Modal;
class Battery extends Component {

  state = {
    isloading: false,
  }

  componentDidMount() {
    this.props.getInuseBattery();
  }

  async handleClickVirtualCard() {
    this.setState({ isloading: true });
    try {
      const { balance, deposit } = await getVirtualCard();
      this.props.updateCount({
        balance,
        deposit,
      });
      hashHistory.push('/balance');
    } catch (error) {
      if (error.status === 400) {
        alert(error.message.message, '确定开通吗？', [
          { text: '取消', style: 'default' },
          { text: '确定', onPress: () => openVirtualCardService() },
        ]);
      }
      this.setState({ isloading: false });
    }
  }

  scan() {
    wx.scanQRCode({
      needResult: 1,
      scanType: ['qrCode', 'barCode'],
      success(res) {
        const result = res.resultStr; // 当needResult 为 1 时，扫码返回的结果
        hashHistory.push(`/usebattery?number=${result}`);
      },
    });
  }

  render() {
    const restTime = 14 - moment().diff(moment(this.props.useDate), 'days');
    return (
      <div>
        <NoticeBar
          mode="link"
          style={{ display: isNaN(restTime) ? 'none' : 'flex' }}
          onClick={() => { }}
        >你正在使用闪充，还有{restTime}天剩余时间，点击归还！
        </NoticeBar>
        <div className={styles.functions}>
          <div className={styles.function} style={{ background: '#8BA6EE' }} onClick={this.scan}>
            <p><Icon type={require('../../assets/image/QR-code.svg')} style={{ width: '.44rem', height: '.44rem' }} /></p>
            <p>扫一扫</p>
          </div>
          <div
            className={styles.function}
            style={{ background: '#FBBBB1' }}
            onClick={() => { this.handleClickVirtualCard(); }}
          >
            <p><Icon type={require('../../assets/image/card.svg')} style={{ width: '.44rem', height: '.44rem' }} /></p>
            <p>消费卡</p>
          </div>
          <div
            className={styles.function}
            style={{ background: '#8FDBBE' }}
            onClick={() => prompt('你要进行保修吗？', '请输入闪充电池编号',
              [
                { text: '取消' },
                {
                  text: '提交',
                  onPress: value => new Promise((resolve) => {
                    batteryReport(value)
                      .then(() => {
                        Toast.success('报修成功!');
                        resolve();
                      })
                      .catch(() => { Toast.info('车辆编号不存在!'); });
                  }),
                },
              ], 'default', null, ['请输入闪充编号'])}
          >
            <p><Icon type={require('../../assets/image/fix.svg')} style={{ width: '.44rem', height: '.44rem' }} /></p>
            <p>闪充保修</p>
          </div>
        </div>
        <Button onClick={this.wxpay}>付款</Button>
        <ActivityIndicator
          toast
          text="加载中..."
          animating={this.state.isloading}
        />
      </div>
    );
  }

  wxpay() {
    wx.chooseWXPay({
      timeStamp: parseInt(new Date().getTime() / 1000) + '', // 支付签名时间戳，注意微信jssdk中的所有使用timestamp字段均为小写。但最新版的支付后台生成签名使用的timeStamp字段名需大写其中的S字符
      nonceStr: Math.random().toString(36).substr(2, 15), // 支付签名随机串，不长于 32 位
      package: 'prepay_id=wx20170912153529308eb36ac90335591882', // 统一支付接口返回的prepay_id参数值，提交格式如：prepay_id=***）
      signType: 'MD5', // 签名方式，默认为'SHA1'，使用新版支付需传入'MD5'
      paySign: '3B278361C28E556E2F2287EED9420FDB', // 支付签名
      success: function (res) {
        // 支付成功后的回调函数
        alert('suceess' + res);
      }
    });
  }
}

const mapStateToProps = (state) => {
  const { battery } = state;
  return {
    useDate: battery.inuseBattery && battery.inuseBattery.useDate,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    updateCount: (account) => { dispatch({ type: 'battery/updateCount', ...account }); },
    getInuseBattery: () => { dispatch({ type: 'battery/getInuseBattery' }); },
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Battery);
