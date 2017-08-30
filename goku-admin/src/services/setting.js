import request from '../utils/request';

export function modifySetting(data) {
  return request({
    method: 'POST',
    url: 'manager/basic_setting/const',
    data,
  });
}

export function getConst() {
  return request.get('manager/basic_setting/const');
}
