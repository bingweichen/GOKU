import React, { Component } from 'react';
import { Picker, List } from 'antd-mobile';
import { hashHistory } from 'dva/router';
import  PropTypes from 'prop-types';
import { connect } from 'dva';
import BuyFooter from '../../components/CarDetail/BuyFooter';
import styles from './OrderDetail.less';

class OrderDetail extends Component {

  state = {
    useCoupons: '',
    note: '',
  }

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

  submitOrder = () => {
    const { orderDetail, carInfo, submitBuyCarOrder } = this.props;
    submitBuyCarOrder({
      e_bike_model: orderDetail.carType,
      color: orderDetail.color,
      category: carInfo.category,
      orderType: '买车',
      note: this.state.note,
      coupon: null,
    });
  }

  render() {
    const { orderDetail, carInfo, coupons } = this.props;
    const { useCoupons } = this.state;
    const rentTime = [{
      value: '1', label: '一个月',
    },
    {
      value: '2', label: '两个月',
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
          <Picker data={rentTime} cols={1}>
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
            <span style={{ float: 'right' }}>￥{carInfo.price}</span>
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
              实付款:￥{carInfo.price - (useCoupons && JSON.parse(useCoupons).value)}
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
    submitBuyCarOrder: (order) => { dispatch({ ...order, type: 'order/submitBuyCarOrder' }); },
  };
};


export default connect(mapStateToProps, mapDispatchToProps)(OrderDetail);
