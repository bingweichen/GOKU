import request from '../utils/request';

export function getCarDataSource({ page, number }) {
  return request.get(`manager/basic_setting/e_bike_model/all?page=${page}&&paginate_by=${number}`);
}

export function addNewCar(data) {
  return request({
    method: 'PUT',
    url: '/manager/basic_setting/e_bike_model',
    data,
  });
}

export function editCar(data) {
  return request({
    method: 'POST',
    url: '/manager/basic_setting/e_bike_model',
    data,
  });
}
