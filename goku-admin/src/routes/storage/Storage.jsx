import React from 'react';
import { Table } from 'antd';
import { connect } from 'dva';
import { storageCol } from '../../utils/Table/columns.js';

const Storage = ({
  dataSource,
  total,
  dispatch,
}) => {
  return (
    <div>
      <Table
        columns={storageCol}
        dataSource={dataSource}
        pagination={{
          total,
          onChange(page, pageSize) {
            dispatch({
              type: 'storage/getDataSource',
              page,
              pageSize,
            });
          },
        }}
      />
    </div>
  );
};

const mapStateToProps = ({ storage }) => {
  return {
    dataSource: storage.dataSource,
    total: storage.total,
  };
};

export default connect(mapStateToProps)(Storage);
