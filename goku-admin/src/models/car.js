import * as service from '../services/car';

export default {

  namespace: 'car',

  state: {
    dataSource: [],
    visible: false,
    inEdit: false,
    record: {},
  },

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
          half_year_price: val.price['学期'],
          year_price: val.price['年'],
          key: val.name,
        })),
      };
    },
    setVisible(state, { visible }) {
      return { ...state, visible };
    },
    setEditStatus(state, { isEdit }) {
      return { ...state, isEdit };
    },
    setRecord(state, { record }) {
      return { ...state, record };
    },
  },
};
