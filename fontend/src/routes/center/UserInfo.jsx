// 用户个人简单信息
import React, { Component } from 'react';
import { List } from 'antd-mobile';
import axios from '../../utils/axios.js';

const Item = List.Item;
class UserInfo extends Component {

  state = {
    user: {},
  }

  componentDidMount() {
    axios('user/get_user_info')
      .then((data) => { this.setState({ user: data }); });
  }
  render() {
    const { user } = this.state;
    return (
      <div>
        <List renderHeader={() => '个人信息'} >
          <Item extra={user.name}>姓名</Item>
          <Item extra={user.username}>用户名</Item>
          <Item extra={user.school}>学校</Item>
          <Item extra={user.phone}>手机号</Item>
          <Item extra={user.student_id}>学号</Item>
        </List>
      </div>
    );
  }
}

export default UserInfo;
