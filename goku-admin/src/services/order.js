import { message } from 'antd';
import request from '../utils/request';

export function order({ page, number, days }) {
  return request.get(`manager/appointment_setting/appointments/all?page=${page}&&paginate_by=${number}` +
    `&&days=${days}`);
}

export function returnBike(bikeData) {
  return request({
    url: 'manager/appointment_setting/appointment/return_e_bike',
    method: 'POST',
    data: bikeData,
  });
}

// 取消订单
export async function cancelOrder(id, user) {
  try {
    await request({
      method: 'POST',
      url: 'manager/appointment_setting/appointment/status/cancel',
      data: {
        username: user,
        appointment_id: id,
        account: '',
        account_type: '',
        comment: '',
      },
    });
    message.success('订单取消成功');
  } catch (error) {
    message.error('订单取消失败');
  }
}

// 手动更改订单状态为已付款
export async function modifyOrderSuccess(id, user) {
  try {
    await request({
      method: 'POST',
      url: 'manager/appointment_setting/appointment/status/total_payment_success',
      data: {
        username: user,
        appointment_id: id,
        account: '',
        account_type: '',
        comment: '',
      },
    });
    message.success('订单状态已更改为成功');
  } catch (error) {
    message.error('操作失败');
  }
}
