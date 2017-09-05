import request from '../utils/request';
import axios from '../utils/axios';

export function getCoupon() {
  return axios('coupon');
}

export function getAllSchool() {
  return request('/api/school');
}

export function register(info) {
  return axios.post('user/register', info);
}

export function getOrder() {
  return axios.get('appointment/all');
}

export function login({ username, password }) {
  return axios({
    method: 'POST',
    url: 'user/login',
    data: {
      username, password,
    },
  });
}
