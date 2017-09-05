import request from '../utils/request';
import axios from '../utils/axios';

export function getCoupon(id) {
  return request(`/api/coupon/${id}`);
}

export function getAllSchool() {
  return request('/api/school');
}

export function register(info) {
  return axios.post('user/register', info);
}

export function getOrder(id) {
  return axios.get(`appointment/all?username=${id}`);
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
