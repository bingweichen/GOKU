import pathToRegexp from 'path-to-regexp';
import * as shopService from '../services/shop';

export default {
  namespace: 'shop',
  state: {
    // id: '',
    image_url: [],
    image_urls: [],
    name: '',
    price: '',
    color: '',
    colors: [],
    num_view: '', // 浏览量
  },
  reducers: {
    // setId(state, action) {
    //   return { ...state, id: action.payload.id };
    // },
    setData(state, action) {
      return { ...state, ...action.payload };
    },
  },
  effects: {
    // fetch car detail message
    *fetch({ payload }, { call, put }) {
      const { data } = yield call(shopService.getCarDetail, payload.id);
      yield put({ type: 'setData', payload: { ...data.response.e_bike_model } });
    },
  },
  subscriptions: {
    // set car id
    setup({ dispatch, history }) {
      return history.listen(({ pathname }) => {
        if (pathToRegexp('/cardetail/:id').exec(pathname)) {
          // dispatch({ type: 'setId', payload: { id: pathname.split('/')[2] } });
          dispatch({ type: 'fetch', payload: { id: pathname.split('/')[2] } });
        }
      });
    },
  },
};
