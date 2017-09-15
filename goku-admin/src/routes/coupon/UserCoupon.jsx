import React, { Component } from 'react';
import { Table, message } from 'antd';
import { UserCouponCol } from '../../utils/Table/columns.js';
import request from '../../utils/request.js';

class UserCoupon extends Component {

  state = {
    dataSource: [],
  }

  componentDidMount() {
    request.get('manager/basic_setting/coupon/all')
      .then((data) => {
        const dataSource = data.map(d => ({ ...d, key: d.id }));
        this.setState({ dataSource });
      })
      .catch(() => message.error('获取数据失败'));
  }

  render() {
    return (
      <div>
        <Table
          columns={UserCouponCol}
          dataSource={this.state.dataSource}
        />
      </div>
    );
  }
}

export default UserCoupon;
