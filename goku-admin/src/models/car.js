import * as service from '../services/car';

export default {

  namespace: 'car',

  state: {},

  subscriptions: {
    setup({ dispatch, history }) {
      return history.listen(({ pathname }) => {
        if (pathname === '/admin/car') {
          dispatch({ type: 'getDataSource', number: 10, page: 1 });
        }
      });
    },
  },

  effects: {
    *getDataSource({ page, number }, { call, put }) {
      const { e_bike_models } = yield call(service.getCarDataSource, { page, number });
      yield put({ type: 'setDataSource', data: e_bike_models });
    },
  },

  reducers: {
    setDataSource(state, { data }) {
      return {
        ...state,
        dataSource: data.map(val => ({
          ...val,
          price: typeof val.price === 'object' ?
            `${val.price['学期']}/学期,${val.price['年']}/年` : val.price,
          key: val.name,
        })),
      };
    },
  },
};
