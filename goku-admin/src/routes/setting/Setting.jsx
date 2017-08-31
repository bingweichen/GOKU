import React, { Component } from 'react';
import { Input, Button, message } from 'antd';
import { modifySetting, getConst } from '../../services/setting';

class Setting extends Component {

  state = {
    allSetting: [],
  }

  componentDidMount() {
    this.fetchData();
  }

  fetchData = () => {
    getConst()
      .then(({ const: allSetting }) => {
        const state = {};
        allSetting.forEach(({ key, value }) => {
          state[key] = value;
        });
        this.setState({ ...state, allSetting });
      })
      .catch(() => message.error('获取数据失败'));
  }

  moditySet = async (key) => {
    try {
      await modifySetting({
        key,
        value: this.state[key],
      });
      message.success('修改成功');
      this.fetchData();
    } catch (error) {
      message.error('修改失败');
    }
  }

  handleInput = (e) => {
    this.setState({
      [e.target.name]: e.target.value,
    });
  }


  render() {
    return (
      <div>
        {
          this.state.allSetting.map(({ label, key }) => (
            <div
              key={key}
              style={{
                display: 'flex',
                margin: 10,
              }}
            >
              <p style={{ width: 200 }}>{label}</p>
              <Input
                style={{ width: 200, marginRight: 20 }}
                type="number"
                name={key} value={this.state[key]} onChange={this.handleInput}
              />
              <Button
                type="primary"
                onClick={() => { this.moditySet(key); }}
              >修改</Button>
            </div>
          ))
        }
      </div>
    );
  }
}

export default Setting;
