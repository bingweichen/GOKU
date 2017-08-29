import request from '../utils/request';

export function getAllRefund() {
  return request('refund_table');
}
