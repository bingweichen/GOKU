import * as carService from '../services/car';

export default {

  namespace: 'IndexPage',

  state: {
    cars: [],
    carType: '小龟',
  },

  subscriptions: {
    setup({ dispatch, history }) {
      return history.listen(({ pathname }) => {
        if (pathname === '/') {
          dispatch({ type: 'getCar' });
        }
      });
    },
  },

  effects: {
    *fetch({ payload }, { put }) {
      yield put({ type: 'save' });
    },
    // 根据车子的类型得到车
    *getCar({ payload }, { call, put, select }) {
      const { carType } = yield select(state => state.IndexPage);
      const { data } = yield call(carService.getCars, carType);
      yield put({
        type: 'loadCar',
        payload: {
          cars: data.response.e_bike_models,
        },
      });
    },
    *changeCarType({ carType }, { put }) { // 改变选择的车类型
      yield put({ type: 'selectCarType', carType });
      yield put({ type: 'getCar' });
    },
  },

  reducers: {
    save(state, action) {
      return { ...state, ...action.payload };
    },
    loadCar(state, action) {
      return { ...state, cars: [...action.payload.cars] };
    },
    selectCarType(state, action) {
      return { ...state, carType: action.carType };
    },

  },

};
