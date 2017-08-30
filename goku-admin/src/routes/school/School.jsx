import React, {Component} from 'react';
import {Table} from 'antd';
import {getAllSchool} from '../../services/school.js';
import {schoolCol} from '../../utils/Table/columns.js';

class School extends Component {
  constructor(props) {
    super(props);
    this.cols = schoolCol.concat([{
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
  }

  state = {
    dataSource: [],
    visible: false,
    isEdit: false,
    selectData: {},
  };

  componentDidMount() {
    this.getDataSource();
  }

  async getDataSource() {
    const {schools} = await getAllSchool();
    this.setState({
      dataSource: schools.map(school => ({
        ...school,
        key: school.name,
      })),
    });
  }

  toggleVisible = (visible, isEdit) => {
    this.setState({visible, isEdit});
  }

  render() {
    const { dataSource, isEdit, visible, selectData } = this.state;

    return (
      <div>
        <Table
          columns={this.cols}
          dataSource={dataSource}
        />
      </div>
    );
  }
}

export default School;
