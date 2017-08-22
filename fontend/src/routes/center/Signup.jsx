import React, { Component } from 'react';
import { createForm } from 'rc-form';
import { List, InputItem, Button, Picker } from 'antd-mobile';
import { hashHistory } from 'dva/router';
import { getAllSchool, register } from '../../services/person';

class Signup extends Component {
  state = {
    username: '',
    password: '',
    name: '',
    phone: '',
    school: '',
    student_id: '',
    identify_number: '',
    schools: [],
    errorText: '',
    loading: false,
  }

  componentDidMount() {
    getAllSchool()
      .then(({ data }) => {
        const schools = data.response.map(school => ({
          label: school.name,
          value: school.name,
        }));
        this.setState({ schools });
      });
  }

  submit = () => {
    this.props.form.validateFields((err, value) => {
      if (err) {
        this.setState({ errorText: '请正确填写信息!' });
      } else if (value.password !== value.repassword) {
        this.setState({ errorText: '两次密码输入不一致' });
      } else {
        this.setState({ errorText: '', loading: true });
        register(value)
          .then(() => {
            this.setState({ errorText: '', loading: false });
            hashHistory.replace('/signin');
          })
          .catch((error) => {
            this.setState({ errorText: error.response.data.response.message, loading: false });
          });
      }
    });
  }

  render() {
    const { getFieldProps, getFieldError } = this.props.form;
    return (
      <div style={{ padding: '0.3rem' }}>
        <List>
          <InputItem
            type="text"
            placeholder=""
            maxLength={10}
            {...getFieldProps('username', {
              rules: [{ required: true }],
            }) }
          >用户名</InputItem>
          <InputItem
            type="password"
            maxLength={12}
            placeholder=""
            {...getFieldProps('password', {
              rules: [{ required: true }],
            }) }
          >密码</InputItem>
          <InputItem
            type="password"
            maxLength={12}
            placeholder=""
            {...getFieldProps('repassword', {
              rules: [{ required: true }],
            }) }
          >确认密码</InputItem>
          <InputItem
            type="text"
            maxLength={12}
            placeholder=""
            {...getFieldProps('name', {
              rules: [{ required: true }],
            }) }
          >姓名</InputItem>
          <InputItem
            type="number"
            maxLength={11}
            placeholder=""
            {...getFieldProps('phone', {
              rules: [{ required: true, pattern: /^1[0-9]{10}$/ }],
            }) }
          >手机号</InputItem>
          <Picker
            format={val => (val[0])}
            data={this.state.schools} cols={1}
            {...getFieldProps('school', {
              rules: [{ required: true }],
            }) }
            className="forss"
          >
            <List.Item arrow="horizontal">选择地区（单列）</List.Item>
          </Picker>
          <InputItem
            type="number"
            {...getFieldProps('student_id', {
              rules: [{ required: true }],
            }) }
          >学号</InputItem>
          <InputItem
            type="text"
            maxLength={18}
            {...getFieldProps('identify_number', {
              rules: [{ required: true, pattern: /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/ }],
            }) }
          >身份证号</InputItem>
        </List>
        <Button
          style={{
            marginTop: '.2rem',
          }}
          loading={this.state.loading}
          type="primary"
          onClick={this.submit}
        >注册</Button>
        <p style={{ textAlign: 'center', color: '#d00a0a' }}>{this.state.errorText}</p>
      </div >
    );
  }
}
const WrapperSignup = createForm()(Signup);

export default WrapperSignup;
