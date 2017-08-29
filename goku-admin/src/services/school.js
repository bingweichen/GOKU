import request from '../utils/request';

export function getAllSchool() {
  return request.get('manager/basic_setting/school/all');
}
