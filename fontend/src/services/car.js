import axios from 'axios';
import request from '../utils/request';

export function getCars(type) {
  const url = `/api/e_bike_model?category=${type}`;
  return axios.get(url);
}

