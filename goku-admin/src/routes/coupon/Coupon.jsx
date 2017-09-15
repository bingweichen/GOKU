import React, { Component } from 'react';
import { Table, Button, message } from 'antd';
import { connect } from 'dva';
import CouponModal from '../../components/Modal/CouponModal';
import { couponCol } from '../../utils/Table/columns.js';
import request from '../../utils/request.js';

const renderCol = [...couponCol, {
  key: 'dispatch',
  title: '给所有人派发优惠券',
  dataIndex: 'dispatch',
  render(text, record) {
    return (
      <Button
        onClick={() => {
          request.put('manager/basic_setting/coupon_to_all_user', {
            template_id: record.id,
          }).then(() => { message.success('派发成功'); })
            .catch(() => message.error('派发失败'));
        }}
      >派发</Button>
    );
  },
},
];
class Coupon extends Component {

  state = {
    visible: false,
  }

  toggleVisible = (visible) => {
    this.setState({
      visible,
    });
  }

  render() {
    const { dataSource } = this.props;
    const { visible } = this.state;
    return (
      <div>
        <CouponModal
          visible={visible}
          toggleVisible={this.toggleVisible}
        />
        <Button
          onClick={
            () => this.toggleVisible(true)
          }
        >
          添加</Button>
        <Table
          columns={renderCol}
          dataSource={dataSource}
        />
      </div >
    );
  }
}

const mapStateToProps = ({ coupon: couponState }) => {
  return {
    dataSource: couponState.dataSource,
  };
};

export default connect(mapStateToProps)(Coupon);
