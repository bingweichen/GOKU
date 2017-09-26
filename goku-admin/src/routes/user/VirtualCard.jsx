import React, { Component } from 'react';
import { Table, message, Button } from 'antd';
import { VirtualCardCol } from '../../utils/Table/columns.js';
import request from '../../utils/request.js';

const colunms = [
  ...VirtualCardCol,
  {
    key: 'operation',
    title: '操作',
    render(text, record) {
      return (
        <div>
          <Button
            onClick={() => removeFreeze(record.card_no)}
            disabled={record.situation !== '冻结'}
          >
            解除冻结
        </Button>
          <Button
            onClick={() => cardAuth(record.card_no)}
            disabled={record.real_name_authentication === '已认证'}
          >
            实名认证
        </Button>
        </div>
      );
    },
  },
];

const removeFreeze = (cardNo) => {
  request(`manager/user_setting/virtual_card/re_freeze?card_no=${cardNo}`)
    .then(() => message.success('解除冻结成功'))
    .catch(() => message.error('解除失败'));
};

const cardAuth = (cardNo) => {
  request(`manager/user_setting/virtual_card/real_name_authentication?card_no=${cardNo}`)
    .then(() => message.success('已完成用户实名认证'))
    .catch(() => message.error('用户实用认证失败'));
};

class VirtualCard extends Component {

  state = {
    dataSource: [],
  }

  componentDidMount() {
    request('manager/user_setting/virtual_cards/all')
      .then(({ virtual_cards }) => {
        this.setState({
          dataSource: virtual_cards.map(data => ({
            ...data,
            key: data.card_no,
          })),
        });
      })
      .catch(() => message.error('获取数据失败'));
  }
  render() {
    return (
      <div>
        <Table
          dataSource={this.state.dataSource}
          columns={colunms}
        />
      </div>
    );
  }
}

export default VirtualCard;
