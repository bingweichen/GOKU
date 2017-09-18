import request from '../utils/request';

export function getAllRefund() {
  return request('manager/support/refund_table/all');
}

export function setRefundStatus(id) {
  return request({
    method: 'POST',
    url: 'manager/support/refund_table/set_success_refund_status',
    data: {
      refund_table_id: id,
    },
  });
}
