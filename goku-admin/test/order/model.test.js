import 'babel-polyfill';
import { expect } from 'chai';
import { put, call } from 'redux-saga/effects';
import * as service from '../../src/services/order';
import order from '../../src/models/order';

describe('test for order', () => {
  describe('effect test', () => {
    const { effects } = order;
    it('test get datasource', () => {
      const gen = effects.getDataSource({ page: 1, number: 10, days: 0 }, { call, put });
      expect(gen.next().value)
        .to.be.deep.equal(call(service.order, { page: 1, number: 10, days: 0 }));
      expect(gen.next().value)
        .to.be.deep.equal(put({ type: 'setDataSource', appointments: [] }));
    });
  });
  describe('reducers test', () => {
    const { reducers } = order;
    it('test set datasource', () => {
      const appointments = [{
        id: 1,
        date: 'Thu Aug 24 2017 22:33:52 GMT+0800 (CST)',
        expired_date_time: 'Thu Aug 24 2017 22:33:52 GMT+0800 (CST)',
      }];
      expect(reducers.setDataSource({}, { appointments })).to.deep.equal({
        appointments: [{
          key: 1,
          id: 1,
          date: '2017/08/24 22:33',
          expired_date_time: '2017/08/24 22:33',
        }],
      });
    });
  });
});
