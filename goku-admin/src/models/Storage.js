import * as service from '../services/storage';

export default {

  namespace: 'storage',

  state: {
    dataSource: [],
    total: 0,
  },

  subscriptions: {
    setup({ dispatch, history }) {
      return history.listen(({ pathname }) => {
        if (pathname === '/admin/storage') {
          dispatch({ type: 'getDataSource', page: 1, pageSize: 10 });
        }
      });
    },
  },

  effects: {
    *getDataSource({ page, pageSize }, { call, put }) {
      const { storage, total } = yield call(service.getStorage, { page, pageSize });
      yield put({ type: 'setDataSource', data: storage, total });
    },
  },

  reducers: {
    save(state, action) {
      return { ...state, ...action.payload };
    },
    setDataSource(state, { data, total }) {
      return {
        ...state,
        total,
        dataSource: data.map(d => ({
          ...d,
          key: d.color + d.model,
        })),
      };
    },
  },

};
