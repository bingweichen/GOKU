import React, { Component } from 'react';
import { Table } from 'antd';
import { getAllBattery } from '../../services/battery.js';
import { batteryCol } from '../../utils/Table/columns.js';

class Battery extends Component {

  state = {
    dataSource: [],
    total: 0,
  }

  componentDidMount() {
    this.getDataSource({ page: 1, pageSize: 10 });
  }

  async getDataSource({ page, pageSize }) {
    const { battery, total } = await getAllBattery({ page, pageSize });
    this.setState({
      total,
      dataSource: battery.map(val => ({
        ...val,
        key: val.serial_number,
      })),
    });
  }

  render() {
    const { dataSource, total } = this.state;
    return (
      <div >
        <Table
          columns={batteryCol}
          dataSource={dataSource}
          pagination={{
            total,
            onChange: (page, pageSize) => {
              this.getDataSource({ page, pageSize });
            },
          }}
        />
      </div >
    );
  }
}

export default Battery;
