import request from '../utils/request';

export function getCoupons() {
  return request('manager/basic_setting/coupon_template/all');
}

export function addCoupon(data) {
  return request({
    method: 'PUT',
    url: 'manager/basic_setting/coupon_template',
    data,
  });
}
