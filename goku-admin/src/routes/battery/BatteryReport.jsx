import React, { Component } from 'react';
import { Table } from 'antd';
import moment from 'moment';
import { getBatteryReport } from '../../services/battery.js';
import { batteryReport } from '../../utils/Table/columns.js';

class BatteryReport extends Component {
  state = {
    dataSource: [],
  }

  componentDidMount() {
    this.setDataSource();
  }

  async setDataSource() {
    const data = await getBatteryReport();
    this.setState({
      dataSource: data.map(val => ({
        ...val,
        key: val.id,
        report_time: moment(val.report_time).format('YYYY/MM/DD HH:mm'),
      })),
    });
  }
  render() {
    const { dataSource } = this.state;
    return (
      <div>
        <Table
          columns={batteryReport}
          dataSource={dataSource}
        />
      </div>
    );
  }
}

export default BatteryReport;
