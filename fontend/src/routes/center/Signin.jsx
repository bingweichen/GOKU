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
          <Button
            onClick={() => {
              wx.scanQRCode({
                needResult: 0, // 默认为0，扫描结果由微信处理，1则直接返回扫描结果，
                scanType: ['qrCode', 'barCode'], // 可以指定扫二维码还是一维码，默认二者都有
                success(res) {
                  alert(res.resultStr); // 当needResult 为 1 时，扫码返回的结果
                },
              });
            }}>二维码</Button>
        </div>
      </div>
    );
  }
}

export default createForm()(connect()(Signin));
