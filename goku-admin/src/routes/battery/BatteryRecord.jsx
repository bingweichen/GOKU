import React, { Component } from 'react';
import { Table, Select, Input } from 'antd';
import moment from 'moment';
import { getBatteryRecord } from '../../services/battery.js';
import { batteryRecord } from '../../utils/Table/columns.js';

const { Option } = Select;
const { Search } = Input;
class BatteryRecord extends Component {
  state = {
    dataSource: [],
    keyWord: '',
    days: 0,
    total: 0,
  }

  componentDidMount() {
    this.setDataSource(1);
  }

  setDataSource = async (page) => {
    const { days, keyWord } = this.state;
    const { records, total } = await getBatteryRecord(days, keyWord, page, 10);
    this.setState({
      total,
      dataSource: records.map(record => ({
        ...record,
        key: record.id,
        rent_date: moment(record.rent_date).format('YYYY/MM/DD HH:mm'),
        return_date: moment(record.return_date).format('YYYY/MM/DD HH:mm'),
      })),
    });
  }

  render() {
    const { dataSource, total } = this.state;
    return (
      <div>
        <div style={{ marginBottom: 20 }}>
          <Select
            defaultValue="0"
            style={{ width: 120 }}
            onChange={(days) => {
              this.setState({ days }, () => this.setDataSource(1));
            }}
          >
            <Option value="0">全部</Option>
            <Option value="1">一天</Option>
            <Option value="7">一周</Option>
            <Option value="31">一个月</Option>
          </Select>
          <Search
            style={{ width: 200, float: 'right' }}
            onSearch={(value) => {
              this.setState({ keyWord: value }, () => this.setDataSource(1));
            }}
          />
        </div>
        <Table
          columns={batteryRecord}
          dataSource={dataSource}
          pagination={{
            total,
            onChange: (page) => {
              this.setDataSource(page);
            },
          }}
        />
      </div>
    );
  }
}

export default BatteryRecord;
