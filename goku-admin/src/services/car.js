import request from '../utils/request';

export function getCarDataSource({ page, number }) {
  return request.get(`manager/basic_setting/e_bike_model/all?page=${page}&&paginate_by=${number}`);
}
