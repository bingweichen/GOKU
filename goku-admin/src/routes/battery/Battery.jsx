import React, { Component } from 'react';
import { Table, Tag, Input } from 'antd';
import QRCode from 'qrcode.react';
import { getAllBattery, getTotalUse, getCurrentUse } from '../../services/battery.js';
import { batteryCol } from '../../utils/Table/columns.js';

const { Search } = Input;
class Battery extends Component {

  state = {
    dataSource: [],
    total: 0,
    totalUse: 0,
    currentUse: 0,
    keyWord: '',
  }

  componentDidMount() {
    this.getDataSource({ page: 1, pageSize: 10, keyWord: '' });
    this.setTotalUse();
    this.setCurrentUse();
  }

  async getDataSource({ page, pageSize, keyWord }) {
    const { battery, total } = await getAllBattery({ page, pageSize, keyWord });
    this.setState({
      total,
      dataSource: battery.map(val => ({
        ...val,
        key: val.serial_number,
      })),
    });
  }

  async setTotalUse() {
    const { total_use } = await getTotalUse();
    this.setState({ totalUse: total_use });
  }

  async setCurrentUse() {
    const { current_use } = await getCurrentUse();
    this.setState({ currentUse: current_use });
  }

  cols = batteryCol.concat({
    title: '二维码',
    dataIndex: 'qrcode',
    render: (text, record) => (
      <QRCode value={record.serial_number} />
    ),
  })

  render() {
    const { dataSource, total, totalUse, currentUse, keyWord } = this.state;
    return (
      <div >
        <div style={{ marginBottom: 20 }}>
          <Tag color="#108ee9">使用闪充的总人数:{totalUse}</Tag>
          <Tag color="#108ee9">当前在使用闪充的人数:{currentUse}</Tag>
          <Search
            placeholder="输入编号搜索"
            style={{ width: 200, float: 'right' }}
            onSearch={(value) => {
              this.setState({ keyWord: value },
                () => this.getDataSource({ page: 1, pageSize: 10, keyWord: value }));
            }}
          />
        </div>
        <Table
          columns={this.cols}
          dataSource={dataSource}
          pagination={{
            total,
            onChange: (page, pageSize) => {
              this.getDataSource({ page, pageSize, keyWord });
            },
          }}
        />
      </div >
    );
  }
}

export default Battery;
