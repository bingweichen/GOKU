import React, {Component} from 'react';
import {Table, Button,
  // Upload, Icon,
  message
} from 'antd';
import {getAllSchool} from '../../services/school.js';
import {schoolCol} from '../../utils/Table/columns.js';
import SchoolModal from '../../components/Modal/SchoolModal';

// // const Dragger = Upload.Dragger;
// const props = {
//   name: 'file',
//   multiple: true,
//   showUploadList: false,
//   action: 'http://ouhx8b81v.bkt.clouddn.com/1111',
//   data: {
//     token: 'v99cBTIFIpr-7MWfgoeAOS4UeNfGkGh8Flgw0s7C:wyCCdoSLF3-4X6rhaO2XUpPxVnc=:eyJzY29wZSI6InF0ZXN0YnVja2V0IiwiZGVhZGxpbmUiOjE1MDQxMjM2NjJ9'
//   },
//   onChange(info) {
//     const status = info.file.status;
//     if (status !== 'uploading') {
//       console.log(info.file, info.fileList);
//     }
//     if (status === 'done') {
//       message.success(`${info.file.name} file uploaded successfully.`);
//     } else if (status === 'error') {
//       message.error(`${info.file.name} file upload failed.`);
//     }
//   },
// };

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

        {/*<div style={{ marginTop: 16, height: 180 }}>*/}
          {/*<Dragger {...props}>*/}
            {/*<p className="ant-upload-drag-icon">*/}
              {/*<Icon type="inbox" />*/}
            {/*</p>*/}
            {/*<p className="ant-upload-text">Click or drag file to this area to upload</p>*/}
            {/*<p className="ant-upload-hint">Support for a single or bulk upload. Strictly prohibit from uploading company data or other band files</p>*/}
          {/*</Dragger>*/}
        {/*</div>*/}

      </div>
    );
  }
}

export default School;
