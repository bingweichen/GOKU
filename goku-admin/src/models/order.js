import moment from 'moment';
import * as service from '../services/order';

export default {

  namespace: 'order',

  state: {
    appointments: [],
  },

  subscriptions: {
    setup({ dispatch, history }) {
      return history.listen(({ pathname }) => {
        if (pathname === '/admin/order') {
          dispatch({ type: 'getDataSource', number: 10, page: 1 });
        }
      });
    },
  },

  effects: {
    *getDataSource({ page, number }, { call, put }) {
      try {
        const { appointments } = yield call(service.order, { page, number });
        yield put({ type: 'setDataSource', appointments });
      } catch (error) {
        yield put({ type: 'setDataSource', appointments: [] });
      }
    },
  },

  reducers: {
    save(state, action) {
      return { ...state, ...action.payload };
    },
    setDataSource(state, { appointments }) {
      const formatData = appointments.map(appointment => ({
        ...appointment,
        key: appointment.id,
        date: moment(appointment.date).format('YYYY/MM/DD HH:mm'),
        expired_date_time: moment(appointment.expired_date_time).format('YYYY/MM/DD HH:mm'),
      }));
      return { ...state, appointments: formatData };
    },
  },

};
