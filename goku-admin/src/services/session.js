import request from '../utils/request';

export function signin({ username, password }) {
  return request({
    method: 'POST',
    url: 'user/manager/login',
    data: {
      username, password,
    },
  });
}
