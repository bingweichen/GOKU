import * as batteryService from '../services/battery';

export default {

  namespace: 'battery',

  state: {
    deposit: 0,
    balance: 0,
    inuseBattery: null,
  },

  subscriptions: {
    setup({ dispatch, history }) {
      return history.listen(({ pathname, query }) => {
        if (pathname === '/balance') {
          dispatch({ type: 'getAccountBattery' });
        }
      });
    },
  },
  effects: {
    *getAccountBattery(action, { call, put }) {
      const { deposit, balance } = yield call(batteryService.getVirtualCard);
      yield put({
        type: 'updateCount',
        deposit,
        balance,
      });
    },
    *getInuseBattery(action, { put, call }) {
      const { battery } = yield call(batteryService.inuseBattery);
      yield put({
        type: 'updateUseBattery',
        useDate: battery.rent_date,
        number: battery.serial_number,
      });
    },
  },

  reducers: {
    // 更新账户信息
    updateCount(state, action) {
      return {
        ...state,
        deposit: action.deposit,
        balance: action.balance,
      };
    },
    // 更新用户使用闪充
    updateUseBattery(state, action) {
      return {
        ...state,
        inuseBattery: {
          useDate: action.useDate,
          number: action.number,
        },
      };
    },
  },
};
