import axios from 'axios';

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

instance.interceptors.response.use((response) => {
  return response.data.response;
}, (error) => {
  const { status, data } = error.response;
  return Promise.reject({ status, message: data.response });
});

export default instance;
