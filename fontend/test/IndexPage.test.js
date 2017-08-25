import 'babel-polyfill';
import { put, call, select } from 'redux-saga/effects';
import { expect } from 'chai';
import IndexPage from '../src/models/IndexPage';
import * as carService from '../src/services/car';


describe('IndexPageModel', () => {
  describe('test effects', () => {
    const effects = IndexPage.effects;
    it('it should fetch data', () => {
      const gen = effects.fetch({}, { put, call });
      expect(gen.next().value).to.deep.equal(put({ type: 'save' }));
      expect(gen.next()).to.deep.equal({ done: true, value: undefined });
    });
    it('it should get car data', () => {
      const gen = effects.getCar({ payload: { carType: '小龟' } }, { call, select, put });
      expect(gen.next().value.SELECT.selector({ IndexPage: '小龟' })).to.equal('小龟');
      expect(gen.next({ carType: '小龟' }).value).to.deep.equal(call(carService.getCars, '小龟'));
      expect(gen.next({ data: { response: { e_bike_models: 123 } } }).value)
        .to.deep.equal(put({
          type: 'loadCar',
          payload: {
            cars: 123,
          },
        }));
    });
  });
  describe('test reducer', () => {
    const reducers = IndexPage.reducers;
    it('it should save data', () => {
      const data = reducers.save({}, { payload: { cars: [{ name: '小龟' }] } });
      expect(data).to.deep.equal({ cars: [{ name: '小龟' }] });
    });
    it('it should load cars', () => {
      expect(reducers.loadCar({}, { payload: { cars: [{ name: '小龟' }] } }))
        .to.deep.equal({ cars: [{ name: '小龟' }] });
    });
    it('it should toggle carType', () => {
      expect(reducers.selectCarType({}, { carType: '小龟' }))
        .to.deep.equal({ carType: '小龟' });
    });
  });
});

