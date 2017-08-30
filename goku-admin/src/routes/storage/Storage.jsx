import React, { Component } from 'react';
import { Table, Button } from 'antd';
import { connect } from 'dva';
import StorageModal from '../../components/Modal/StorageModal';
import { storageCol } from '../../utils/Table/columns.js';

class Storage extends Component {
  state = {
    visible: false,
    isEdit: false,
    selectData: {},
  }

  toggleVisible = (visible) => {
    this.setState({ visible });
  }

  render() {
    const { dataSource, total, dispatch } = this.props;
    const { visible, isEdit } = this.state;
    const cols = storageCol.concat([
      {
        title: '操作',
        dataIndex: 'detail',
        render: (text, record) => (
          <Button
            onClick={() => {
              this.setState({
                isEdit: true,
                selectData: record,
                visible: true,
              });
            }}
          >
            编辑
          </Button>
        ),
      },
    ]);
    return (
      <div>
        <Button
          type="primay"
          onClick={() => {
            this.toggleVisible(true);
            this.setState({
              isEdit: false,
              selectData: {},
            });
          }}
        >增加</Button>
        <StorageModal
          visible={visible}
          toggleVisible={this.toggleVisible}
          isEdit={isEdit}
          data={this.state.selectData}
        />
        <Table
          columns={cols}
          dataSource={dataSource}
          pagination={{
            total,
            onChange(page, pageSize) {
              dispatch({
                type: 'storage/getDataSource',
                page,
                pageSize,
              });
            },
          }}
        />
      </div >
    )
  }
}

const mapStateToProps = ({ storage }) => {
  return {
    dataSource: storage.dataSource,
    total: storage.total,
  };
};

export default connect(mapStateToProps)(Storage);
