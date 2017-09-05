import React, { Component } from 'react';
import { Toast, InputItem, Button } from 'antd-mobile';
import { connect } from 'dva';
import { createForm } from 'rc-form';
import styles from './signin.less';

class Signin extends Component {

  submit = () => {
    this.props.form.validateFields((error, value) => {
      console.log(value)
      if (error) {
        Toast.fail('用户名或密码不能为空');
      } else {
        this.props.dispatch({
          ...value,
          type: 'person/login',
        });
      }
    });
  }

  render() {
    const { getFieldProps } = this.props.form;

    return (
      <div>
        <div className={styles.logoContainer}>
          <img src={require("../../assets/image/logo.png")} alt="" />
        </div>
        <div>
          <InputItem
            {...getFieldProps('username', {
              rules: [{ required: true }],
            }) }
            type="text"
            placeholder="输入你的用户名"
          >用户名</InputItem>
          <InputItem
            {...getFieldProps('password', {
              rules: [{ required: true }],
            }) }
            type="password"
            placeholder="****"
          >密码</InputItem>
          <Button style={{ margin: '.3rem' }} type="primary" onClick={this.submit}>登录</Button>
        </div>
      </div>
    );
  }
}

export default createForm()(connect()(Signin));
