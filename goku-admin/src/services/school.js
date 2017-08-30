import request from '../utils/request';

export function getAllSchool() {
  return request.get('manager/basic_setting/school/all');
}


export function addNewSchool(data) {
  return request({
    method: 'PUT',
    url: 'manager/basic_setting/school',
    data,
  });
}


export function editSchool(data) {
  return request({
    method: 'POST',
    url: 'manager/basic_setting/school',
    data,
  });
}
