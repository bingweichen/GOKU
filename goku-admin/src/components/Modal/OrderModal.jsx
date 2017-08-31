import React, { Component } from 'react';
import { Modal, Button, message } from 'antd';
import { returnBike, cancelOrder, modifyOrderSuccess } from '../../services/order.js';


// 付款之后改变订单状态 xx => success
// const handleChangeStatus = async () => {
//   try {
//     await modifyOrderStatus({

//     });
//     message.success('订单状态更改失败');
//   } catch (error) {
//     message.error('订单更改状态失败');
//   }
// }

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
          <div style={{ display: 'flex', justifyContent: 'center', flexDirection: 'column' }}>
            {
              record.type === '租车' && record.status === '待归还' ?
                <Button
                  type="primary"
                  style={{ margin: 10 }}
                  onClick={() => { this.handleReturn(record.id, record.serial_number); }}
                > 如果用户已还车，请点击此处进行还车操作</Button> : ''
            }
            {
              (record.status !== '取消') &&
                (record.status !== '交易成功') &&
                (record.status !== '待还车') ? <Button
                  type="primary"
                  style={{ margin: 10 }}
                  onClick={() => { cancelOrder(record.id, record.user); }}
                > 点击此处进行订单的取消,(取消、交易成功、待还车不可取消订单)</Button> : ''
            }
            {
              (record.status === '待付款') ||
                (record.status === '待付预约款') ? <Button
                  type="primary"
                  style={{ margin: 10 }}
                  onClick={() => { modifyOrderSuccess(record.id, record.user); }}
                > 如果用户已经付款，点击此处更改用户已付款状态</Button> : ''
            }
          </div>
        </div>
      </Modal>
    );
  }
}

export default OrderModal;
