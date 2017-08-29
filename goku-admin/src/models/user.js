import * as service from '../services/user';

export default {

  namespace: 'user',

  state: {
    dataSource: [],
  },

  subscriptions: {
    setup({ dispatch, history }) {
      return history.listen(({ pathname }) => {
        if (pathname === '/admin/user') {
          dispatch({ type: 'getDataSource' });
        }
      });
    },
  },

  effects: {
    *getDataSource(action, { call, put }) {
      const { users } = yield call(service.getUsersInfo);
      yield put({ type: 'setDataSource', users });
    },
  },

  reducers: {
    save(state, action) {
      return { ...state, ...action.payload };
    },
    setDataSource(state, { users }) {
      return {
        ...state,
        dataSource: users.map(user => ({
          ...user,
          key: user.username,
        })),
      };
    },
  },

};
