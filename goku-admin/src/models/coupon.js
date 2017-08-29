import * as service from '../services/coupon';

export default {

  namespace: 'coupon',

  state: {
    dataSource: [],
  },

  subscriptions: {
    setup({ dispatch, history }) {
      return history.listen(({ pathname }) => {
        if (pathname === '/admin/coupons') {
          dispatch({ type: 'getDataSource' });
        }
      });
    },
  },

  effects: {
    *getDataSource(action, { call, put }) {
      const data = yield call(service.getCoupons);
      yield put({ type: 'setDataSource', data });
    },
  },

  reducers: {
    setDataSource(state, { data }) {
      return {
        ...state,
        dataSource: data.map(d => ({
          ...d,
          key: d.id,
        })),
      };
    },
  },

};
