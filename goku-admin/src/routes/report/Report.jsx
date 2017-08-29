import React, { Component } from 'react';
import { Table } from 'antd';
import { formatDate } from '../../utils/Time.js';
import { getAllReport } from '../../services/report.js';
import { reportCol } from '../../utils/Table/columns.js';

class Report extends Component {
  state = {
    dataSource: [],
  }
  componentDidMount() {
    this.setDataSource();
  }

  async setDataSource() {
    const data = await getAllReport();
    this.setState({
      dataSource: data.map(val => ({
        ...val,
        key: val.id,
        date: formatDate(val.date),
      })),
    });
  }
  render() {
    const { dataSource } = this.state;
    return (
      <div>
        <Table
          dataSource={dataSource}
          columns={reportCol}
        />
      </div>
    );
  }
}

export default Report;
