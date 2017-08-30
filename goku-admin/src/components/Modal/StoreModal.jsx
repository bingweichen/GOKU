import React, { Component } from 'react';
import { Modal, Input, message, Button } from 'antd';
import { addNewStore, editStore, delStore } from '../../services/store.js';

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

  submitInput = async (isEdit) => {
    try {
      if (isEdit) {
        await editStore(this.state);
      } else {
        await addNewStore(this.state);
      }
      message.success('操作成功');
    } catch (error) {
      message.error('操作失败');
    }
  }

  handleDel = async (name) => {
    try {
      await delStore(name);
      message.success('操作成功');
    } catch (error) {
      message.error('删除失败');
    }
  }

  render() {
    const { visible, toggleVisible, isEdit, data } = this.props;
    const stores = [
      { value: 'name', label: '名称', disabled: isEdit },
      { value: 'address', label: '地址' },
    ];

    return (
      <Modal
        visible={visible}
        onCancel={() => toggleVisible(false)}
        footer={[
          <Button
            key="cancel"
            onClick={isEdit ? () => this.handleDel(data.name) : () => toggleVisible(false)}
          >
            {isEdit ? '删除' : '取消'}</Button>,
          <Button
            type="primary"
            key="ok" onClick={() => this.submitInput(isEdit)}
          >确定</Button>,
        ]}
      >
        <div>
          {
            stores.map(({ value, label, disabled }) => (
              <div key={value}>
                <span>{label}</span>
                <Input
                  value={this.state[value]}
                  onChange={this.handleInput}
                  name={value}
                  disabled={disabled}
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
