import 'babel-polyfill';
import { expect } from 'chai';
import { put, call } from 'redux-saga/effects';
import * as service from '../src/services/order';
import order from '../src/models/order';

describe('test for order', () => {
  describe('effect test', () => {
    const { effects } = order;
    it('test get datasource', () => {
      const gen = effects.getDataSource({ page: 1, number: 10 }, { call, put });
      expect(gen.next().value).to.be.deep.equal(call(service.order, { page: 1, number: 10 }));
      // expect(gen.next().done).to.be.equal(false);
      // expect(gen.next().done).to.be.equal(false);
      expect(gen.next().value).to.be.deep.equal(put({ type: 'setDataSource', appointments: [] }));
    });
  });
});
