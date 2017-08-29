import React, { Component } from 'react';
import { Table, Select } from 'antd';
import moment from 'moment';
import { getBatteryRecord } from '../../services/battery.js';
import { batteryRecord } from '../../utils/Table/columns.js';

const { Option } = Select;
class BatteryRecord extends Component {
  state = {
    dataSource: [],
  }

  componentDidMount() {
    this.setDataSource(0);
  }

  async setDataSource(days) {
    const { records } = await getBatteryRecord(days);
    this.setState({
      dataSource: records.map(record => ({
        ...record,
        key: record.id,
        rent_date: moment(record.rent_date).format('YYYY/MM/DD HH:mm'),
        return_date: moment(record.return_date).format('YYYY/MM/DD HH:mm'),
      })),
    });
  }

  render() {
    const { dataSource } = this.state;
    return (
      <div>
        <Select
          defaultValue="0"
          style={{ width: 120 }}
          onChange={(days) => {
            this.setDataSource(days);
          }}
        >
          <Option value="0">全部</Option>
          <Option value="1">一天</Option>
          <Option value="7">一周</Option>
          <Option value="31">一个月</Option>
        </Select>
        <Table
          columns={batteryRecord}
          dataSource={dataSource}
        />
      </div>
    );
  }
}

export default BatteryRecord;
