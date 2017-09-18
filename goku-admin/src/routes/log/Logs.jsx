import React, { Component } from 'react';
import { Table, message } from 'antd';
import moment from 'moment';
import request from '../../utils/request.js';

const colunms = [
  { title: '类别', key: 'category', dataIndex: 'category' },
  { title: '请求开始', key: 'start', dataIndex: 'start' },
  { title: '请求结束', key: 'end', dataIndex: 'end' },
  {
    title: '请求',
    children: [{
      title: '方式',
      key: 'method',
      dataIndex: 'request.method',
    },
    { title: '路径', key: 'route', dataIndex: 'request.route' },
    { title: '值', key: 'values', dataIndex: 'request.values' },
    ],
  },
  { title: '返回状态', key: 'status', dataIndex: 'response.status' },
];

class Logs extends Component {

  state = {
    dataSource: [],
  }
  componentDidMount() {
    request('manager/support/logs')
      .then(({ logs }) => {
        const dataSource = logs.map(log => ({
          ...log,
          key: log.id,
          start: moment(log.start).format('YYYY/MM/DD HH:mm '),
          end: moment(log.end).format('YYYY/MM/DD HH:mm'),
        }));
        this.setState({ dataSource });
      })
      .catch(() => message.error('获取数据失败'));
  }

  render() {
    return (
      <div>
        <Table
          columns={colunms}
          dataSource={this.state.dataSource}
        />
      </div>
    );
  }
}

export default Logs;
