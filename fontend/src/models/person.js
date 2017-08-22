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
  },
  effects: {
    // 得到优惠卷
    *getCoupons(action, { call, put, select }) {
      const { person } = yield select();
      const { data } = yield call(personService.getCoupon, person.id);
      yield put({ type: 'setCoupons', coupons: data.response });
    },
    // 得到用户订单
    *getOrder(action, { call, put, select }) {
      const { person } = yield select();
      try {
        const { data } = yield call(personService.getOrder, person.id);
        yield put({ type: 'setUserOrder', appointments: data.response.appointments });
      } catch (error) {
        console.log(error);
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
