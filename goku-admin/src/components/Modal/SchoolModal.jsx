/**
 * Created by chen on 2017/8/30.
 */
import React, { Component } from 'react';
import { Modal, Input } from 'antd';

class SchoolModal extends Component {

  state = {
    name: '',
    address: '',
  }

  componentWillReceiveProps(nextProps) {
    const { name, address } = nextProps.data;
    this.setState({
      name, address,
    });
  }


  handleInput = (e) => {
    this.setState({
      [e.target.name]: e.target.value,
    });
  }

  submitInput = () => {
    // if(isEdit)
  }

  render() {
    const { visible, toggleVisible } = this.props;
    const schools = [
      { value: 'name', label: '名称' },
      { value: 'address', label: '地址' },
      { value: 'store', label: '所属商铺' },
    ];
    return (
      <Modal
        visible={visible}
        onCancel={() => toggleVisible(false)}
      >
        <div>
          {
            schools.map(({ value, label }) => (
              <div key={value}>
                <span>{label}</span>
                <Input
                  value={this.state[value]}
                  onChange={this.handleInput}
                  name={value}
                />
              </div>
            ))
          }
        </div>
      </Modal>
    );
  }
}

export default SchoolModal;
