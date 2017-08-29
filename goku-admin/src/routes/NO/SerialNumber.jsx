import React, { Component } from 'react';
import { Table } from 'antd';
import { getAllSerialNumber } from '../../services/NO.js';
import { serialNumber } from '../../utils/Table/columns.js';

class SerialNumber extends Component {

  state = {
    dataSource: [],
    total: 0,
  }

  componentDidMount() {
    this.setDataSource({ page: 1, pageSize: 10 });
  }

  async setDataSource({ page, pageSize }) {
    const { serial_number, total } = await getAllSerialNumber({ page, pageSize });
    this.setState({
      total,
      dataSource: serial_number.map(val => ({
        ...val,
        key: val.code,
        available: val.available ? '未占用' : '占用',
      })),
    });
  }

  render() {
    const { dataSource, total } = this.state;
    return (
      <div>
        <Table
          columns={serialNumber}
          dataSource={dataSource}
          pagination={{
            total,
            onChange: (page, pageSize) => {
              this.setDataSource({ page, pageSize });
            },
          }}
        />
      </div>
    );
  }
}

export default SerialNumber;
