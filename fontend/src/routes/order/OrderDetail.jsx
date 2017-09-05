import React, { Component } from 'react';
import { Picker, List } from 'antd-mobile';
import { hashHistory } from 'dva/router';
import PropTypes from 'prop-types';
import { connect } from 'dva';
import BuyFooter from '../../components/CarDetail/BuyFooter';
import styles from './OrderDetail.less';

class OrderDetail extends Component {

  state = {
    useCoupons: '',
    note: '',
    selectType: ['学期'], // 租用时间
  }

  // 优惠卷
  getUserCoupons(coupons) {
    const formatCoupons = [];
    coupons.forEach((val) => {
      if (val.situation <= parseInt(this.props.carInfo.price, 10)) {
        formatCoupons.push({
          label: val.desc,
          value: JSON.stringify({
            id: val.id,
            value: val.value,
          }),
        });
      }
    });
    return formatCoupons;
  }

  // 提交订单
  submitOrder = () => {
    const { orderDetail, carInfo, submitBuyCarOrder, location } = this.props;
    const { useCoupons } = this.state;
    const { type } = location.query; // 判断为买车还是租车
    const submitData = {
      e_bike_model: orderDetail.carType,
      color: orderDetail.color,
      category: carInfo.category,
      type: '买车',
      note: this.state.note,
      coupon: useCoupons ? JSON.parse(useCoupons).id : null,
    };
    if (type === 'rent') {
      submitData.type = '租车';
      submitData.rent_time_period = this.state.selectType[0];
    }
    submitBuyCarOrder(submitData);
  }

  render() {
    const { orderDetail, carInfo, coupons } = this.props;
    const { price } = carInfo;
    const { useCoupons, selectType } = this.state;
    const rentTime = [{
      value: '学期', label: '一学期',
    },
    {
      value: '年', label: '一年',
    }];
    const convey = [{
      value: '自提', label: '自提',
    }];

    return (
      <div className={styles.container}>
        <div className={styles.iteminfo}>
          <div style={{ width: '2rem', height: '2rem' }}>
            <img src={carInfo.image_urls[0]} alt="" style={{ maxWidth: '100%' }} />
          </div>
          <div className={styles.itemdec}>
            <p className={styles.name}>{orderDetail.carType}</p>
            <p className={styles.size}>选择的颜色:{orderDetail.color}</p>
          </div>
        </div>
        <div className={styles.item} style={{ display: orderDetail.type === 'rent' ? 'block' : 'none' }}>
          <Picker
            data={rentTime}
            cols={1}
            value={selectType}
            onChange={(val) => { this.setState({ selectType: val }); }}
          >
            <List.Item arrow="horizontal">租用时间</List.Item>
          </Picker>
        </div>
        <div className={styles.item}>
          <Picker data={convey} cols={1} value={['自提']}>
            <List.Item arrow="horizontal">配送方式</List.Item>
          </Picker>
        </div>
        <div className={styles.item}>
          <Picker
            dismissText="不使用优惠卷"
            onDismiss={() => { this.setState({ useCoupons: '' }); }}
            onChange={(val) => { this.setState({ useCoupons: val }); }}
            data={this.getUserCoupons(coupons)} cols={1} value={useCoupons}
          >
            <List.Item arrow="horizontal">可用优惠卷:</List.Item>
          </Picker>
        </div>
        <div className={styles.item} style={{ padding: 25 }}>
          <span>备注信息</span>
          <div style={{ border: '.01rem solid #979797', marginTop: '.2rem', padding: 10 }}>
            <textarea
              onChange={(e) => { this.setState({ note: e.target.value }); }}
              name="" id="" cols="30" rows="10" style={{ width: '100%', border: 'none' }}
            />
          </div>
        </div>
        <div className={styles.item} style={{ padding: '.2rem' }}>
          <p
            style={{
              color: '#333333',
              fontSize: '0.25rem',
            }}
          >
            <span >商品总额:</span>
            <span style={{ float: 'right' }}>
              ￥{typeof price === 'number' ? price : price[selectType]}
            </span>
          </p>
          <p
            style={{
              color: '#333333',
              fontSize: '0.25rem',
              display: useCoupons ? 'block' : 'none',
            }}
          >
            <span >使用优惠卷:</span>
            <span style={{ float: 'right' }}>-{useCoupons && JSON.parse(useCoupons).value}RMB</span>
          </p>
          <p style={{ overflow: 'hidden' }}>
            <span className={styles.payprice}>
              实付款:￥
              {typeof price === 'number' ? price : price[selectType] - (useCoupons && JSON.parse(useCoupons).value)}
            </span>
          </p>
        </div>
        <BuyFooter
          title="立即预约(预约金￥100)"
          // todo: wechat pay
          onClick={() => { this.submitOrder(); }}
        />
      </div>
    );
  }
}

const mapStateToProps = (state) => {
  const { order, person } = state;
  return {
    carInfo: order.carInfo,
    orderDetail: order.orderDetail,
    coupons: person.coupons,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    getCoupons: () => { dispatch({ type: 'order/getCoupons' }); },
    submitBuyCarOrder: (order) => { dispatch({ submitData: order, type: 'order/submitBuyCarOrder' }); },
  };
};


export default connect(mapStateToProps, mapDispatchToProps)(OrderDetail);
