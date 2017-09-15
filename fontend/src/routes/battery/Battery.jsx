import React, { Component } from 'react';
import { NoticeBar, Icon, Modal, ActivityIndicator, Toast, Button } from 'antd-mobile';
import moment from 'moment';
import { connect } from 'dva';
import { hashHistory } from 'dva/router';
import axios from '../../utils/axios.js';
import { getVirtualCard, openVirtualCardService, batteryReport } from '../../services/battery.js';
import styles from './index.less';

const { alert, prompt, operation } = Modal;
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

  scan = () => {
    if (this.props.useDate) { // 正在使用闪充,停止扫描
      Toast.fail('你现在不能再次使用闪充');
    }
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
          style={{ display: this.props.useDate ? 'flex' : 'none' }}
          onClick={ // 归还闪充
            () => operation([
              {
                text: '确定归还',
                onPress: () => {
                  axios.post('battery_rent/return', {
                    serial_number: this.props.number,
                  }).then(() => { Toast.success('还车成功'); window.location.reload(); })
                    .catch((error) => { Toast.fail(error.message.message); });
                },
              },
              { text: '取消' },
            ])
          }
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
        <ActivityIndicator
          toast
          text="加载中..."
          animating={this.state.isloading}
        />
      </div >
    );
  }

}

const mapStateToProps = (state) => {
  const { battery } = state;
  return {
    useDate: battery.inuseBattery && battery.inuseBattery.useDate, // 正在使用的电动车
    number: battery.inuseBattery && battery.inuseBattery.number,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    updateCount: (account) => { dispatch({ type: 'battery/updateCount', ...account }); },
    getInuseBattery: () => { dispatch({ type: 'battery/getInuseBattery' }); },
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Battery);
