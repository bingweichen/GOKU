import React, { Component } from 'react';
import { Table } from 'antd';
import { connect } from 'dva';
import { order as orderConstant } from '../utils/constant';

const colunms = Object.keys(orderConstant).map((key) => {
  return {
    key,
    title: orderConstant[key],
    dataIndex: key,
  };
});

class Order extends Component {

  render() {
    const { dispatch, total } = this.props;
    return (
      <div>
        <Table
          columns={colunms}
          dataSource={this.props.dataSource}
          loading={this.props.loading}
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
}

const mapStateToProps = (state) => {
  return {
    loading: state.loading.global,
    dataSource: state.order.appointments,
  };
};

export default connect(mapStateToProps)(Order);
