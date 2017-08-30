import React, { Component } from 'react';
import { Table, Button } from 'antd';
import StoreModal from '../../components/Modal/StoreModal';
import { getAllStore } from '../../services/store.js';
import { storeCol } from '../../utils/Table/columns.js';

class Store extends Component {
  state = {
    dataSource: [],
    visible: false,
    isEdit: false,
    selectData: {},
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

  toggleVisible = (visible, isEdit) => {
    this.setState({ visible, isEdit });
  }

  render() {
    const { dataSource, isEdit, visible, selectData } = this.state;
    const cols = storeCol.concat([{
      title: '操作',
      dataIndex: 'detail',
      render: (text, record) => (
        <Button
          onClick={() => {
            this.toggleVisible(true, true);
            this.setState({
              selectData: record,
            });
          }}
        >编辑</Button>
      ),
    }]);
    return (
      <div>
        <StoreModal
          visible={visible}
          toggleVisible={this.toggleVisible}
          isEdit={isEdit}
          data={selectData}
        />
        <Button
          onClick={() => {
            this.toggleVisible(true, false);
            this.setState({
              selectData: {},
            });
          }}
        >
          添加</Button>
        <Table
          columns={cols}
          dataSource={dataSource}
        />
      </div>
    );
  }
}

export default Store;
