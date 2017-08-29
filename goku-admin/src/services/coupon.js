import request from '../utils/request';

export function getCoupons() {
  return request('manager/basic_setting/coupon_template/all');
}
