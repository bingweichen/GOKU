import React from 'react';
import { Table } from 'antd';
import { connect } from 'dva';
import { carConstant } from '../../utils/constant.js';
import constructionDS from '../../utils/Table/constructionDS.js';

const columns = constructionDS(carConstant);

function Car({
  dataSource,
  loading,
  total,
  dispatch,
}) {
  return (
    <div>
      <Table
        dataSource={dataSource}
        columns={columns}
        loading={loading}
        pagination={{
          onChange(page, pageSize) {
            dispatch({
              page,
              type: 'car/getDataSource',
              number: pageSize,
            });
          },
          total,
        }}
      />
    </div>
  );
}

const mapStateToProps = ({
  loading: { global },
  car: {
    dataSource,
  },
}) => {
  return {
    dataSource,
    loading: global,
    total: 30,
  };
};

export default connect(mapStateToProps)(Car);
