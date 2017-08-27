import { expect } from 'chai';
import constructionDS from '../../src/utils/Table/constructionDS';

describe('test table function', () => {
  it('test construction datasource for obj', () => {
    expect(constructionDS({
      title: '标题',
    })).to.deep.equal([{
      key: 'title',
      title: '标题',
      dataIndex: 'title',
    }]);
  });
});
