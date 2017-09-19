import React, { Component } from 'react';
import { connect } from 'dva';
import { hashHistory } from 'dva/router';
import { Modal, Toast, InputItem } from 'antd-mobile';
import { payDeposit, ercharge } from '../../services/battery.js';
import axios from '../../utils/axios.js';
import Button from '../../components/Button';
import { wxpay } from '../../wechat';
import styles from './index.less';

const { alert, prompt } = Modal;
class Balance extends Component {
  state = {
    chargeMoney: '',
  }

  setChargeMoney = (value) => {
    if (value && (value.charAt(0) === '0' || value.indexOf('.') >= 0)) {
      this.setState({
        chargeMoney: value.replace(/^0*(\d*).*$/, '$1'),
      });
    } else {
      this.setState({ chargeMoney: value });
    }
  }
  handleRecharge = () => {
    const { chargeMoney } = this.state;
    if (this.props.deposit === 0 || this.props.deposit < 199) {
      alert('还未完成押金充值', '确认充值押金吗？', [
        { text: '取消' },
        {
          text: '确定',
          onPress: () => {
            payDeposit(199)
              .then((info) => {
                wxpay(info, () => { alert('付款成功'); });
                // this.props.updateCount(card.deposit, balance);
              });
          },
        },
      ]);
      return;
    }
    //  wechat pay recharge

    if (chargeMoney <= 0 || chargeMoney.length <= 0) {
      Toast.fail('请输入正确的金额');
      return;
    }
    ercharge(chargeMoney)
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
        <InputItem
          onChange={this.setChargeMoney}
          value={this.state.chargeMoney}
          placeholder="输入你要充值的金额"
          type="number"
          style={{ margin: '10px 0' }}
        >充值</InputItem>
        <Button style={{ width: '100%' }} onClick={this.handleRecharge}>充值</Button>
        <Button
          style={{ width: '100%', marginTop: '.5rem' }}
          onClick={() => hashHistory.push('/expenserecord')}
        >消费记录</Button>
        <div>
          <p style={{ textAlign: 'center', fontSize: '.28rem' }}>
            <span style={{ color: '#616060' }}>押金{deposit}元</span>
            <a
              onClick={() => {
                alert('确定退还押金吗？', '需要确认之后才可以到账', [
                  { text: '取消', onPress: () => console.log('cancel') },
                  {
                    text: '确定',
                    onPress: () => {
                      axios.post('virtual_card/deposit/return_deposit')
                        .then(() => { Toast.success('押金退还成功'); })
                        .catch(() => { Toast.fail('押金退还失败'); });
                    },
                  },
                ]);
              }}
              style={{ color: 'rgb(255, 91, 85)', marginLeft: '.28rem' }}
            >退还押金</a>
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

