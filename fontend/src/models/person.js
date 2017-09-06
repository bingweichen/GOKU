import { Toast } from 'antd-mobile';
import { hashHistory } from 'dva/router';
import * as personService from '../services/person';

export default {
  namespace: 'person',
  state: {
    name: '',
    id: 'bingwei',
    coupons: [],
    orders: [],
  },
  reducers: {
    // 设置优惠卷
    setCoupons(state, action) {
      return {
        ...state,
        coupons: action.coupons,
      };
    },
    // 处理server获取的订单
    setUserOrder(state, action) {
      const orders = action.appointments.map(order => {
        return {
          ...order,
          user: {},
        };
      });
      return {
        ...state,
        orders,
      };
    },
    // 设置用户信息
    setUserInfo(state, { name }) {
      return {
        ...state,
        name,
      };
    },
  },
  effects: {
    // 得到优惠卷
    *getCoupons(action, { call, put }) {
      const coupons = yield call(personService.getCoupon);
      yield put({ type: 'setCoupons', coupons });
    },
    // 得到用户订单
    *getOrder(action, { call, put }) {
      try {
        const { appointments } = yield call(personService.getOrder);
        yield put({ type: 'setUserOrder', appointments });
      } catch (error) {
        console.log(error);
      }
    },
    // 登录
    *login({ username, password }, { call, put }) {
      Toast.loading('正在登录...');
      try {
        const { token, user } = yield call(personService.login, { username, password });
        yield localStorage.setItem('token', `Bearer ${token}`);
        yield put({
          type: 'setUserInfo',
          ...user,
        });
        Toast.hide();
        hashHistory.replace('/');
      } catch (error) {
        Toast.info(error.message.message);
      }
    },
  },
  subscriptions: {
    setup({ dispatch, history }) {
      return history.listen(({ pathname }) => {
        if (pathname === '/coupons') {
          dispatch({ type: 'getCoupons' });
        }
      });
    },
  },
};
