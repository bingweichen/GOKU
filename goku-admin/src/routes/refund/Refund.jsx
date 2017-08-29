import React, { Component } from 'react';
import { Table } from 'antd';
import { formatDate } from '../../utils/Time.js';
import { getAllRefund } from '../../services/refund.js';
import { refundCol } from '../../utils/Table/columns.js';

class Refund extends Component {
  state = {
    dataSource: [],
  }

  componentDidMount() {
    this.setDataSource();
  }

  async setDataSource() {
    const { refund_tables } = await getAllRefund();
    this.setState({
      dataSource: refund_tables.map(val => ({
        ...val,
        date: formatDate(val.date),
        key: val.id,
      })),
    });
  }

  render() {
    const { dataSource } = this.state;
    return (
      <div>
        <Table
          columns={refundCol}
          dataSource={dataSource}
        />
      </div>
    );
  }
}

export default Refund;
