import axios from 'axios';
import { Toast } from 'antd-mobile';
import { hashHistory } from 'dva/router';

Promise.prototype.finally = function (callback) {
  const P = this.constructor;
  return this.then(
    value => P.resolve(callback()).then(() => value),
    reason => P.resolve(callback()).then(() => { throw reason; }),
  );
};

const instance = axios.create({
  baseURL: '/api/',
});

instance.interceptors.request.use((config) => {
  if (config.headers.Authorization === undefined) {
    config.headers.Authorization = localStorage.getItem('token');
  }
  return config;
}, (error) => {
  return Promise.reject(error);
},
);

instance.interceptors.response.use((response) => {
  return response.data.response;
}, (error) => {
  const { status, data } = error.response;
  if (status === 422) { // 用户未登录时
    Toast.fail('请先登录', 2, () => {
      hashHistory.push('signin');
    });
  }
  return Promise.reject({ status, message: data.response });
});

export default instance;
