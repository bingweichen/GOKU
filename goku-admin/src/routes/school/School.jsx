import React, {Component} from 'react';
import {Table, Button} from 'antd';
import {getAllSchool} from '../../services/school.js';
import {schoolCol} from '../../utils/Table/columns.js';
import SchoolModal from '../../components/Modal/SchoolModal';

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
    const {dataSource, isEdit, visible, selectData} = this.state;

    return (
      <div>
        <SchoolModal
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
          columns={this.cols}
          dataSource={dataSource}
        />
      </div>
    );
  }
}

export default School;
