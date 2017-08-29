import React, { Component } from 'react';
import { Table } from 'antd';
import { getAllStore } from '../../services/store.js';
import { storeCol } from '../../utils/Table/columns.js';

class Store extends Component {
  state = {
    dataSource: [],
  }

  componentDidMount() {
    this.getDataSource();
  }

  async getDataSource() {
    const { stores } = await getAllStore();
    this.setState({
      dataSource: stores.map(store => ({
        ...store,
        key: store.name,
      })),
    });
  }

  render() {
    const { dataSource } = this.state;
    return (
      <div>
        <Table
          columns={storeCol}
          dataSource={dataSource}
        />
      </div>
    );
  }
}

export default Store;
