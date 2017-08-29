import React, { Component } from 'react';
import { Table } from 'antd';
import { getAllSchool } from '../../services/school.js';
import { schoolCol } from '../../utils/Table/columns.js';

class School extends Component {
  state = {
    dataSource: [],
  }

  componentDidMount() {
    this.getDataSource();
  }

  async getDataSource() {
    const { schools } = await getAllSchool();
    this.setState({
      dataSource: schools.map(school => ({
        ...school,
        key: school.name,
      })),
    });
  }

  render() {
    return (
      <div>
        <Table
          columns={schoolCol}
          dataSource={this.state.dataSource}
        />
      </div>
    );
  }
}

export default School;
