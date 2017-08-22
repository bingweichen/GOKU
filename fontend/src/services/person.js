import request from '../utils/request';
import axios from 'axios';

export function getCoupon(id) {
  return request(`/api/coupon/${id}`);
}

export function getAllSchool() {
  return request('/api/school');
}

export function register(info) {
  return axios.post('/api/user/register', info);
}

export function getOrder(id) {
  return axios.get(`/api/appointment/all?username=${id}`);
}
