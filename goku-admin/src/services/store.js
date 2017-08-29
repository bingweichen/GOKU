import request from '../utils/request';

export function getAllStore() {
  return request.get('manager/basic_setting/store/all');
}
