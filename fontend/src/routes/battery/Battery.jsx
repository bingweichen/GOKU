import React, { Component } from 'react';
import { NoticeBar, Icon, Modal, ActivityIndicator, Toast } from 'antd-mobile';
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

  render() {
    const restTime = 14 - moment().diff(moment(this.props.useDate), 'days');
    return (
      <div>
        <NoticeBar
          mode="link"
          style={{ display: isNaN(restTime) ? 'none' : 'block' }}
          onClick={() => { }}
        >
          你正在使用闪充，还有{restTime}天剩余时间，点击归还！
        </NoticeBar>
        <div className={styles.functions}>
          <div className={styles.function} style={{ background: '#8BA6EE' }}>
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
      </div>
    );
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
