import axios from '../axios';
import getUrlParam from '../getUrlParam';

export default async function () {
  if (!localStorage.getItem('openid')) {
    const code = getUrlParam('code', location.href);
    const { open_id } = await axios.post(`wx/code_to_openid?code=${code}`);
    localStorage.setItem('openid', open_id);
  }
  try {
    // if (!sessionStorage.getItem('head') || !localStorage.getItem('token')) {
    const data = await axios.get(`user/openid_login?openid=${localStorage.getItem('openid')}`);
    localStorage.setItem('username', data.user.username);
    sessionStorage.setItem('head', data.wx_user.headimgurl);
    // }
  } catch (error) {
    if (error.status === 400) { // 用户未注册

    }
  }
}
