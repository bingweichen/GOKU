import request from '../utils/request';
import axios from 'axios';

export function getCars(type) {
  const url = `/api/e_bike_model?category=${type}`;
  console.log(url);
  return axios.get(url);
}

