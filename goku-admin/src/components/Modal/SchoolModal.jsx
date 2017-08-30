/**
 * Created by chen on 2017/8/30.
 */
import React, {Component} from 'react';
import {Modal, Input, message} from 'antd';
import { addNewSchool, editSchool } from '../../services/school.js';


class SchoolModal extends Component {

  state = {
    name: '',
    address: '',
    store: ''
  }

  componentWillReceiveProps(nextProps) {
    const {name, address, store} = nextProps.data;
    this.setState({
      name, address, store
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

  submit = () => {
    try {
      if (this.props.isEdit) {
        this.handleEditSchool(this.state);
      } else {
        this.addNewSchool(this.state);
      }
    } catch (error) {
      message.error('操作失败');
    }
  }

  async addNewSchool(data) {
    await addNewSchool(data);
    message.success('添加成功');
    this.props.toggleVisible(false);
  }

  async handleEditSchool(data) {
    await editSchool(data);
    message.success('修改成功');
    this.props.toggleVisible(false);
  }

  render() {
    const {visible, toggleVisible, isEdit} = this.props;
    const schools = [
      {value: 'name', label: '名称'},
      {value: 'address', label: '地址'},
      {value: 'store', label: '所属商铺'},
    ];
    if (isEdit){
      schools[0]["disabled"]=true
    }

    return (
      <Modal
        visible={visible}
        onCancel={() => toggleVisible(false)}
        onOk={() => { this.submit(); }}
      >
        <div>
          {
            schools.map(({value, label, disabled}) => (
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

export default SchoolModal;
