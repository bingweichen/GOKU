import React, { Component } from 'react';
import { Modal, Input } from 'antd';

class StoreModal extends Component {

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
    const stores = [
      { value: 'name', label: '名称' },
      { value: 'address', label: '地址' },
    ];
    return (
      <Modal
        visible={visible}
        onCancel={() => toggleVisible(false)}
      >
        <div>
          {
            stores.map(({ value, label }) => (
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

export default StoreModal;
