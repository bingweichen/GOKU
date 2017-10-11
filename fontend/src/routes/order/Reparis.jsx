// 订单中车辆维修的页面
import React, { Component } from 'react';
import { InputItem, Button, Toast } from 'antd-mobile';
import { hashHistory } from 'dva/router';
import { repariCar } from '../../services/order.js';

class Reparis extends Component {

  state = {
    address: '',
    comment: '',
    phone: '',
  }
  handleChange = (value, name) => {
    this.setState({
      [name]: value,
    });
  }

  submit = () => {
    const reason = {
      ...this.state,
      appointment: this.props.location.query.id,
    };
    repariCar(reason)
      .then(() => {
        Toast.info('报修成功', 1, () => {
          hashHistory.push('/?tab=order');
        });
      })
      .catch(() => {
        Toast.fail('报修失败');
      });
  }

  render() {
    return (
      <div style={{ padding: 25 }}>
        <p style={{ fontSize: 28 }}>上门维修统一收取20元上门维修费，实体店维修请自行持身份证到店铺维修</p>
        <InputItem
          placeholder="输入你的地址"
          onChange={(value) => { this.handleChange(value, 'address'); }}
        >
          你的地址
        </InputItem>
        <InputItem
          placeholder="保修原因"
          onChange={(value) => { this.handleChange(value, 'comment'); }}
        >保修原因</InputItem>
        <InputItem
          placeholder="手机号"
          onChange={(value) => { this.handleChange(value, 'phone'); }}
        >手机号</InputItem>
        <Button
          onClick={this.submit}
          type="primary" style={{ marginTop: 50 }}> 提交保修</Button>
      </div>
    );
  }
}

export default Reparis;
