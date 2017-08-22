import request from '../utils/request';

export function getCarDetail(id) {
  return request(`/api/e_bike_model/${id}`);
}
