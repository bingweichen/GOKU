import 'babel-polyfill';
import { effects } from 'dva/saga';
import IndexPage from '../src/models/IndexPage';
import { expect } from 'chai';

describe('IndexPageModel', function () {
  it('it should fetch data', function () {
    const gen = IndexPage.effects.fetch({}, { put, call });
    console.log(gen.next().value)
    // expect(fetch.next().value).to.deep.equal(put({ type: 'save' }));
  })
});
