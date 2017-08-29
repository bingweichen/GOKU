import 'babel-polyfill';
import { expect } from 'chai';
import { put, call } from 'redux-saga/effects';
import * as service from '../../src/services/user';
import user from '../../src/models/user';

describe('test for user', () => {
  describe('effect test', () => {
    const { effects } = user;
    it('it should get datasource', () => {
      const gen = effects.getDataSource({}, { call, put });
      expect(gen.next().value).to.deep.equal(call(service.getUsersInfo));
    });
  });
});
