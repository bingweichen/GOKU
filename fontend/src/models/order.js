import pathToRegexp from 'path-to-regexp';
import parse from 'url-parse';
import { hashHistory } from 'dva/router';
import * as shopService from '../services/shop';
import * as orderService from '../services/order';
import { wxpay } from '../wechat';

export default {
  namespace: 'order',
  state: {
    orderDetail: {
      type: '',
      carType: '',
      color: '',
    },
    carInfo: {
      image_urls: [],
      price: 0,
    },
    // 拥有的优惠券
    coupons: [],
    pickUpSite: { // 自提点
      adviceSite: {}, // 建议自提点
      allSite: [], // 所有自提点
    },
  },
  reducers: {
    // 设置车的基本信息
    setCarInfo(state, action) {
      return {
        ...state,
        orderDetail: action.orderDetail,
        carInfo: action.carInfo,
      };
    },

    // 设置自提点
    setPickUpSite(state, { advice_store, stores }) {
      return {
        ...state,
        pickUpSite: {
          adviceSite: advice_store,
          allSite: stores,
        },
      };
    },
  },
  effects: {
    // 设置订单选择的信息
    *setOrderDetail({ orderDetail }, { call, put }) {
      const { data } = yield call(shopService.getCarDetail, orderDetail.carType);
      const carInfo = data.response.e_bike_model;
      yield put({ type: 'setCarInfo', carInfo, orderDetail });
      yield put({ type: 'person/getCoupons' });
    },

    // 获取自提点
    *getPickUpSite(action, { select, call, put }) {
      const { person } = yield select();
      const { data } = yield call(orderService.getPickUpSite, person.id);
      yield put({ type: 'setPickUpSite', ...data.response });
    },
    // 提交买车预订
    *submitBuyCarOrder(action, { select, call }) {
      const { person } = yield select();
      const { submitData } = action;
      try {
        const { id } = yield call(orderService.buyCarOrder, submitData, person.id);
        // todo wechat pay
        const info = yield call(orderService.paySuccess, id);
        wxpay(info, hashHistory.replace('/?tab=order'));
      } catch (error) {
        console.log(error);
      }
    },
  },
  subscriptions: {
    setup({ dispatch, history }) {
      return history.listen(({ pathname }) => {
        if (pathname === '/orderdetail') {
          const url = parse(window.document.URL.replace('#/', ''), true);
          dispatch({
            type: 'setOrderDetail',
            orderDetail: {
              type: url.query.type,
              carType: url.query.carType,
              color: url.query.color,
            },
          });
        } else if (pathname === '/pickupsite') {
          dispatch({ type: 'getPickUpSite' });
        }
      });
    },
  },
};
