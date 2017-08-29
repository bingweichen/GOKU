import React from 'react';
import { Table } from 'antd';
import { connect } from 'dva';
import { couponCol } from '../../utils/Table/columns.js';

const coupon = ({
  dataSource,
}) => {
  return (
    <div>
      <Table
        columns={couponCol}
        dataSource={dataSource}
      />
    </div>
  );
};

const mapStateToProps = ({ coupon: couponState }) => {
  return {
    dataSource: couponState.dataSource,
  };
};

export default connect(mapStateToProps)(coupon);
