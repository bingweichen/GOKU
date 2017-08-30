import React, { Component } from 'react';
import { Modal, Input, message } from 'antd';
import { addStorage, editStorage } from '../../services/storage.js';

const initState = {
  model: '',
  color: '',
  num: '',
};

class StorageModal extends Component {

  state = initState;

  componentWillReceiveProps(nextProps) {
    const { color, model, num } = nextProps.data;
    this.setState({
      model, color, num,
    });
  }

  handleInput = (e) => {
    this.setState({
      [e.target.name]: e.target.value,
    });
  }

  async handleSubmit(isEdit, data) {
    try {
      if (isEdit) {
        await editStorage(data);
      } else {
        await addStorage(data);
      }
      this.props.toggleVisible(false);
      message.success('操作成功');
    } catch (error) {
      message.error('操作失败');
    }
  }

  render() {
    const { visible, toggleVisible, isEdit } = this.props;
    const inputs = [
      { value: 'model', label: '电动车型号' },
      { value: 'color', label: '颜色' },
      { value: 'num', label: '数量' },
    ];
    return (
      <Modal
        visible={visible}
        onCancel={() => toggleVisible(false)}
        onOk={() => { this.handleSubmit(isEdit, this.state); }}
      >
        <div>
          {
            inputs.map(({ value, label }) => (
              <div key={value}>
                <span>{label}</span>
                <Input name={value} value={this.state[value]} onChange={this.handleInput} />
              </div>
            ))
          }

        </div>
      </Modal>
    );
  }
}

export default StorageModal;
