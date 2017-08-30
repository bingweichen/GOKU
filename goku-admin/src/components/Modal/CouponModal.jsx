import React, { Component } from 'react';
import { Modal, Input, message } from 'antd';
import { addCoupon } from '../../services/coupon.js';

const inputs = [
  { value: 'situation', label: '使用条件(满多少)' },
  { value: 'value', label: '减免价格' },
  { value: 'duration', label: '有效时间(天)' },
  { value: 'desc', label: '描述' },
];

const submitInput = async (data) => {
  try {
    await addCoupon(data);
    message.success('操作成功');
  } catch (error) {
    message.error('操作失败');
  }
}

class CouponModal extends Component {

  state = {

  }

  handleInput = (e) => {
    this.setState({
      [e.target.name]: e.target.value,
    });
  }

  render() {
    const { visible, toggleVisible } = this.props;
    return (
      <Modal
        visible={visible}
        onCancel={() => toggleVisible(false)}
        onOk={() => { submitInput(this.state); }}
      >
        {
          inputs.map(({ value, label }) => (
            <div key={value}>
              <span>{label}</span>
              <Input
                name={value}
                value={this.state[value]}
                onChange={this.handleInput}
              />
            </div>
          ))
        }
      </Modal>
    );
  }
}

export default CouponModal;
