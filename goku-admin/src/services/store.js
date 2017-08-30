import request from '../utils/request';

export function getAllStore() {
  return request.get('manager/basic_setting/store/all');
}

export function addNewStore(data) {
  return request({
    method: 'PUT',
    url: 'manager/basic_setting/store',
    data,
  });
}
