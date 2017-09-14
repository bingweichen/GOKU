import React, { Component } from 'react';
import { Toast } from 'antd-mobile';
import { connect } from 'dva';
import { hashHistory } from 'dva/router';
import { pickUpWithCarNumber, paySuccess } from '../../services/order.js';
import Button from '../../components/Button';
import StepInput from '../../components/StepInput';
import { wxpay } from '../../wechat';

class PickUpCar extends Component {
  state = {
    number: '',
    id: this.props.location.query.id,
    isLoading: false,
  }

  setNumber = (value) => {
    this.setState({ number: value });
  }

  pickUpCarInputNumber = () => {
    if (this.state.number.length < 6 || this.state.isLoading) {
      return;
    }
    Toast.loading('等待付款', 0);
    this.setState({ isLoading: true });
    pickUpWithCarNumber({
      appointment_id: parseInt(this.state.id, 10),
      serial_number: this.state.number,
    })
      .then(() => {
        this.setState({ isLoading: false });
        // todo : 微信支付
        Toast.hide();
        paySuccess(parseInt(this.state.id, 10),
        )
          .then((data) => {
            wxpay(data, () => { hashHistory.replace('/pickupsuccess'); });
          });
      })
      .catch(({ message }) => {
        this.setState({ isLoading: false });
        Toast.hide();
        Toast.fail(message.message);
      });
  }

  render() {
    return (
      <div>
        <div style={{ padding: '0.7rem' }}>
          <p style={{ fontSize: '.24rem', marginBottom: '.6rem' }} > 请输入电动车编号</p>
          <StepInput
            setValue={this.setNumber}
            value={this.state.number}
          />
          <Button
            onClick={() => { this.pickUpCarInputNumber(); }}
            style={{ margin: '.5rem auto', width: '100%' }}
          >付款并提车</Button>
        </div>
      </div>
    );
  }
}

const mapStateToProps = (state) => {
  const { person } = state;
  return {
    username: person.id,
  };
};

export default connect(mapStateToProps)(PickUpCar);
