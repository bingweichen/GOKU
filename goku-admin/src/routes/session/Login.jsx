import React, { Component } from 'react';
import { Form, Icon, Input, Button, Message } from 'antd';
import { connect } from 'dva';
import { hashHistory } from 'dva/router';
import { signin } from '../../services/session.js';
import styles from './Login.less';

const FormItem = Form.Item;
class Login extends Component {
  handleSubmit = (e) => {
    e.preventDefault();
    this.props.form.validateFields((err, values) => {
      if (!err) {
        signin(values)
          .then(({ token }) => {
            localStorage.setItem('token', `Bearer ${token}`);
            hashHistory.push('/admin/order');
          })
          .catch(({ message }) => Message.error(message.message));
      }
    });
  }

  render() {
    const { getFieldDecorator } = this.props.form;
    return (
      <div className={styles.container}>
        <video
          src={require('../../assets/img/flowers.mp4')}
          autoPlay="autoplay"
          loop="loop"
          className={styles.video}
          muted="muted"
        />
        <Form onSubmit={this.handleSubmit} className={styles.loginForm}>
          <FormItem>
            {getFieldDecorator('username', {
              rules: [{ required: true, message: '请输入用户名' }],
            })(
              <Input prefix={<Icon type="user" style={{ fontSize: 13 }} />} placeholder="用户名" />,
            )}
          </FormItem>
          <FormItem>
            {getFieldDecorator('password', {
              rules: [{ required: true, message: '请输入你的密码!' }],
            })(
              <Input prefix={<Icon type="lock" style={{ fontSize: 13 }} />} type="password" placeholder="密码" />,
            )}
          </FormItem>
          <FormItem>
            <Button type="primary" htmlType="submit" className={styles.loginFormButton}>
              登录
          </Button>
          </FormItem>
        </Form>
      </div>
    );
  }
}

export default connect()(Form.create()(Login));
