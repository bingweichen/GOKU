import React, { Component } from 'react';
import { Table, Button } from 'antd';
import { connect } from 'dva';
import CouponModal from '../../components/Modal/CouponModal';
import { couponCol } from '../../utils/Table/columns.js';

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
          columns={couponCol}
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
