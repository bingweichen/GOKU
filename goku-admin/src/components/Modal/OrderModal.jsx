import React, { Component } from 'react';
import { Modal, Button, message } from 'antd';
import { returnBike } from '../../services/order.js';

class OrderModal extends Component {

  async handleReturn(id, number) {
    try {
      await returnBike({
        appointment_id: id,
        serial_number: number,
        account: '11',
        account_type: '11',
        comment: 'test',
      });
      message.success('还车操作成功');
      this.props.toggleModal({ visible: false });
    } catch (error) {
      message.error('还车操作失败');
    }
  }

  render() {
    const { visible, toggleModal, record } = this.props;
    return (
      <Modal
        visible={visible}
        onCancel={() => { toggleModal({ visible: false }); }}
      >
        <div>
          <div style={{ display: 'flex', justifyContent: 'center' }}>
            {
              record.type === '租车' && record.status === '待归还' ?
                <Button
                  type="primary"
                  onClick={() => { this.handleReturn(record.id, record.serial_number); }}
                > 如果用户已还车，请点击此处进行还车操作</Button> : ''
            }
          </div>
        </div>
      </Modal>
    );
  }
}

export default OrderModal;
