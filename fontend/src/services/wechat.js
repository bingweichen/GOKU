import axios from '../utils/axios';

export function getWxConfig(url) {
  return axios.get(`wx/get_sign?url=${url}`);
}
