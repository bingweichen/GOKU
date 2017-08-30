import request from '../utils/request';

export function getAllRefund() {
  return request('refund_table');
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
