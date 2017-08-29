import React, { Component } from 'react';
import { Table, Select } from 'antd';
import { connect } from 'dva';
import { order as orderConstant } from '../utils/constant';

const { Option } = Select;
const colunms = Object.keys(orderConstant).map((key) => {
  return {
    key,
    title: orderConstant[key],
    dataIndex: key,
  };
});

class Order extends Component {
  state = {
    selectDay: '0',
  }

  render() {
    const { dispatch, total } = this.props;
    const handleChange = (day) => {
      this.setState({ selectDay: day });
      dispatch({
        page: 1,
        type: 'order/getDataSource',
        number: 10,
        days: day,
      });
    };
    return (
      <div>
        <div
          style={{
            display: 'flex',
            justifyContent: 'flex-end',
          }}
        >
          <Select
            defaultValue={this.state.selectDay}
            style={{ width: 120 }}
            onChange={handleChange}
          >
            <Option value="0">全部</Option>
            <Option value="1">一天</Option>
            <Option value="7">一周</Option>
            <Option value="30">一个月</Option>
          </Select>
        </div>
        <Table
          columns={colunms}
          dataSource={this.props.dataSource}
          loading={this.props.loading}
          pagination={{
            onChange(page, pageSize) {
              dispatch({
                page,
                type: 'order/getDataSource',
                number: pageSize,
                days: this.state.selectDay,
              });
            },
            total,
          }}
        />
      </div >
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
