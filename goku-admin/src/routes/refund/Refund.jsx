import React, { Component } from 'react';
import { Table, Button, message } from 'antd';
import { formatDate } from '../../utils/Time.js';
import { getAllRefund, setRefundStatus } from '../../services/refund.js';
import { refundCol } from '../../utils/Table/columns.js';


const dealRefundStatus = async (id) => {
  try {
    await setRefundStatus(id);
    message.success('处理成功');
  } catch (error) {
    message.error('处理失败');
  }
};

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

  async

  cols = refundCol.concat([{
    title: '操作',
    dataIndex: 'operation',
    render: (text, record) => (
      record.status === '未处理' ?
        <Button
          onClick={() => dealRefundStatus(record.id)}
          type="primary">确认退款</Button> :
        <span>已处理</span>
    ),
  }])

  render() {
    const { dataSource } = this.state;
    return (
      <div>
        <Table
          columns={this.cols}
          dataSource={dataSource}
        />
      </div>
    );
  }
}

export default Refund;
