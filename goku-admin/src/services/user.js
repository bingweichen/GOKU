import request from '../utils/request';

export function getUsersInfo() {
  return request('manager/user_setting/users/all');
}
