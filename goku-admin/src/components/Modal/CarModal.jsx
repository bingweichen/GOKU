import React, { Component } from 'react';
import { Modal, Input, Select, message } from 'antd';
import { addNewCar, editCar } from '../../services/car.js';

const { Option } = Select;
const initState = {
  name: '',
  configure: '',
  battery: '',
  distance: '',
  category: '',
  type: '',
  half_year_price: '',
  year_price: '',
  colors: [],
  image_urls: [],
  introduction_image_urls: [],
};
class CarModal extends Component {

  state = initState;

  componentWillReceiveProps(nextProps) {
    if (nextProps.isEdit) {
      const {
        name, configure, battery, distance, introduction_image_urls,
        price, category, type, colors, image_urls, half_year_price, year_price } = nextProps.record;
      this.setState({
        name,
        configure,
        battery,
        distance,
        price,
        category,
        type,
        colors,
        image_urls,
        introduction_image_urls,
        half_year_price,
        year_price,
      });
    } else {
      this.setState({
        ...initState,
      });
    }
  }

  handleInput = (e) => {
    const { name } = e.target;
    let { value } = e.target;
    if (name === 'price') {
      value = parseFloat(value);
    }
    this.setState({
      [name]: value,
    });
  }

  submit = () => {
    try {
      if (this.props.isEdit) {
        this.handleEditCar(this.state);
      } else {
        this.addNewCar(this.state);
      }
    } catch (error) {
      message.error('操作失败');
    }
  }

  async addNewCar(data) {
    await addNewCar(data);
    message.success('添加成功');
    this.props.toggleVisible(false);
  }

  async handleEditCar(data) {
    await editCar(data);
    message.success('修改成功');
    this.props.toggleVisible(false);
  }
  render() {
    const { visible, toggleVisible, isEdit } = this.props;
    const arr = [
      { value: 'name', label: '名称', disabled: isEdit },
      { value: 'configure', label: '配置' },
      { value: 'battery', label: '电池' },
      { value: 'distance', label: '续航' },
      // { value: 'price', label: '价格' },
      { value: 'category', label: '种类' },
      { value: 'type', label: '买或租车' },
    ];
    const prices = [
      { value: 'price', label: '价格' },
      { value: 'year_price', label: '每年价格' },
      { value: 'half_year_price', label: '每学期价格' },
    ];
    return (
      <Modal
        visible={visible}
        onCancel={() => { toggleVisible(false); }}
        onOk={() => { this.submit(); }}
      >
        <div>
          {
            arr.map(({ label, value, disabled }) => {
              return (
                <div key={value}>
                  <span>{label}</span>
                  <Input
                    disabled={disabled}
                    name={value}
                    value={this.state[value]}
                    onChange={this.handleInput}
                  />
                </div>
              );
            })
          }
          {
            prices.map(({ value, label }) => (
              <div key={value}>
                <span>{label}</span>
                <Input
                  type="number"
                  name={value}
                  value={this.state[value]}
                  onChange={this.handleInput}
                />
              </div>
            ))
          }
          <div>
            <span>颜色</span>
            <Select
              mode="tags"
              style={{ width: '100%' }}
              placeholder="输入颜色之后按空格确定"
              onChange={(value) => { this.setState({ colors: value }); }}
              value={this.state.colors}
            />
          </div>
          <div>
            <span>轮播图片</span>
            <Select
              mode="tags"
              style={{ width: '100%' }}
              placeholder="输入之后按空格确定"
              onChange={(value) => { this.setState({ image_urls: value }); }}
              value={this.state.image_urls}
            />
          </div>
          <div>
            <span>产品介绍</span>
            <Select
              mode="tags"
              style={{ width: '100%' }}
              placeholder="输入之后按空格确定"
              onChange={(value) => { this.setState({ introduction_image_urls: value }); }}
              value={this.state.introduction_image_urls}
            />
          </div>
        </div>
      </Modal >
    );
  }
}

export default CarModal;
