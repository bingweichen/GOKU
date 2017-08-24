import 'babel-polyfill';
import { expect } from 'chai';
import battery from '../src/models/battery';


describe('expect', () => {
  describe('test reducers for battery', () => {
    const reducers = battery.reducers;
    it('it should update balance', () => {
      expect(reducers.updateCount({}, { deposit: 100, balance: 100 }))
        .to.be.deep.equal({ deposit: 100, balance: 100 });
    });
    it('it should update inuse battery', () => {
      expect(reducers.updateUseBattery({}, { useDate: 'Wed, 23 Aug 2017 07:18:28 GMT', number: 123456 }))
        .to.be.deep.equal({ inuseBattery: { useDate: 'Wed, 23 Aug 2017 07:18:28 GMT', number: 123456 } });
    });
  });
});
