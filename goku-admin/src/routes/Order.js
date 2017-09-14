import React, { Component } from 'react';
import { Table, Select, Button } from 'antd';
import { connect } from 'dva';
import OrderModal from '../components/Modal/OrderModal.jsx';
import { order as orderConstant } from '../utils/constant';

const { Option } = Select;
const colunms = Object.keys(orderConstant).map((key) => {
  return {
    key,
    title: orderConstant[key],
    dataIndex: key,
  };
});

class Order extends Component {
  state = {
    selectDay: '0',
    modalData: {},
  }

  componentDidMount() {

  }

  render() {
    const { dispatch, total, visible, toggleModal } = this.props;
    const handleChange = (day) => {
      this.setState({ selectDay: day });
      dispatch({
        page: 1,
        type: 'order/getDataSource',
        number: 10,
        days: day,
      });
    };
    const cols = colunms.concat([{
      title: '操作',
      dataIndex: 'detail',
      render: (text, record) => {
        return (
          <Button
            type="primary"
            onClick={() => {
              this.props.toggleModal({ visible: true });
              this.setState({ modalData: record });
            }}
          >详情</Button>
        );
      },
    }]);
    return (
      <div>
        <OrderModal
          visible={visible}
          toggleModal={toggleModal}
          record={this.state.modalData}
        />
        <div
          style={{
            display: 'flex',
            justifyContent: 'flex-end',
          }}
        >
          <Select
            defaultValue={this.state.selectDay}
            style={{ width: 120 }}
            onChange={handleChange}
          >
            <Option value="0">全部</Option>
            <Option value="1">一天</Option>
            <Option value="7">一周</Option>
            <Option value="30">一个月</Option>
          </Select>
        </div>
        <Table
          columns={cols}
          dataSource={this.props.dataSource}
          loading={this.props.loading}
          pagination={{
            onChange: (page, pageSize) => {
              dispatch({
                page,
                type: 'order/getDataSource',
                number: pageSize,
                days: this.state.selectDay,
              });
            },
            total,
          }}
        />
      </div >
    );
  }
}

const mapStateToProps = ({ loading, order }) => {
  return {
    loading: loading.global,
    dataSource: order.appointments,
    visible: order.visible,
    total: order.total,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    toggleModal({ visible }) {
      dispatch({
        type: 'order/toggleModalVisible',
        visible,
      });
    },
    dispatch,
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Order);
