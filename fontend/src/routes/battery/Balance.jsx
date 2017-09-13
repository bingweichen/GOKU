import React, { Component } from 'react';
import { connect } from 'dva';
import { hashHistory } from 'dva/router';
import { Modal } from 'antd-mobile';
import { payDeposit, ercharge } from '../../services/battery.js';
import Button from '../../components/Button';
import styles from './index.less';

const { alert } = Modal;
class Balance extends Component {

  handleRecharge = () => {
    if (this.props.deposit === 0 || this.props.deposit < 199) {
      alert('还未完成押金充值', '确认充值押金吗？', [
        { text: '取消' },
        {
          text: '确定',
          onPress: () => {
            payDeposit(199)
              .then(({ data }) => {
                const { balance, card } = data.response;
                this.props.updateCount(card.deposit, balance);
              });
          },
        },
      ]);
      return;
    }
    // wechat pay recharge
    ercharge(0.01)
      .then((info) => {
        wx.chooseWXPay({
          timestamp: info.timeStamp,
          nonceStr: info.nonceStr,
          package: info.package,
          signType: info.signType,
          paySign: info.paySign,
          success(res) {
            alert(`success:${res}`);
          },
        });
        // this.props.updateCount(record.card.deposit, record.balance);
      })
      .catch(() => {
      });
  }

  render() {
    const { balance, deposit } = this.props;
    return (
      <div style={{ padding: '0 .5rem' }}>
        <div className={styles.money}>
          <p style={{ fontSize: '.28rem' }}>账户余额(元)</p>
          <p style={{ fontSize: '1.2rem', margin: 0 }}>{balance}</p>
        </div>
        <Button style={{ width: '100%' }} onClick={this.handleRecharge}>充值</Button>
        <Button
          style={{ width: '100%', marginTop: '.5rem' }}
          onClick={() => hashHistory.push('/expenserecord')}
        >消费记录</Button>
        <div>
          <p style={{ textAlign: 'center', fontSize: '.28rem' }}>
            <span style={{ color: '#616060' }}>押金{deposit}元</span>
            <a style={{ color: 'rgb(255, 91, 85)', marginLeft: '.28rem' }}>退还押金</a>
          </p>
        </div>
      </div >
    );
  }
}

const mapStateToProps = (state) => {
  const { battery } = state;
  return {
    balance: battery.balance,
    deposit: battery.deposit,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    updateCount: (deposit, balance) => dispatch({ type: 'battery/updateCount', deposit, balance }),
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Balance);

