import React, { Component } from 'react';
import { Button } from 'antd-mobile';
import styles from './OrderDetail.less';
import { getOrder } from '../../services/order.js';

class WatchOrder extends Component {

  state = {
    orderId: this.props.location.query.id,
    order: {
      e_bike_model: {
        image_urls: [],
      },
    },
  }

  componentDidMount() {
    getOrder(localStorage.token, this.state.orderId)
      .then(({ data }) => {
        this.setState({ order: data.response.appointment });
      });
  }

  render() {
    const { order } = this.state;
    return (
      <div className={styles.container}>
        <div className={styles.iteminfo}>
          <div style={{ width: '2rem', height: '2rem' }}>
            <img src={order.e_bike_model.image_urls[0]} alt="" style={{ maxWidth: '100%' }} />
          </div>
          <div className={styles.itemdec}>
            <p className={styles.name}>{order.e_bike_model.name}</p>
            <p className={styles.size}>{order.color}色,</p>
          </div>
        </div>

        <div className={styles.iteminfo} style={{ height: 'auto' }}>
          <p style={{ width: '2rem', margin: 0 }}>租用时间:</p>
          <p style={{ flex: 1, margin: 0, color: '#666666' }}>2017-09-01 至2018-09-01 </p>
        </div>

        <div className={styles.iteminfo} style={{ height: 'auto' }}>
          <p style={{ width: '2rem', margin: 0 }}>配送方式:</p>
          <p style={{ flex: 1, margin: 0, color: '#666666' }}>自提 </p>
        </div>

        <div className={styles.iteminfo} style={{ height: 'auto' }}>
          <p style={{ width: '2rem', margin: 0 }}>备注信息:</p>
          <p style={{ flex: 1, margin: 0, color: '#666666' }}>自提自提自提自提自提自提自提自提自提自提自提自提自提自提自提自提自提自提自提自提自提自提自提自提自提自提自提自提自提自提 </p>
        </div>

        <div className={styles.iteminfo} style={{ height: 'auto' }}>
          <p style={{ width: '2rem', margin: 0 }}>下单时间:</p>
          <p style={{ flex: 1, margin: 0, color: '#666666' }}>123 </p>
        </div>

        <div className={styles.item} style={{ padding: '.2rem' }}>
          <p
            style={{
              color: '#333333',
              fontSize: '0.25rem',
            }}
          >
            <span >商品总额:</span>
            <span style={{ float: 'right' }}>￥{123}</span>
          </p>
          <p
            style={{
              color: '#333333',
              fontSize: '0.25rem',
            }}
          >
            <span >使用优惠卷:</span>
            <span style={{ float: 'right' }}>-{123}RMB</span>
          </p>
          <p style={{ overflow: 'hidden' }}>
            <span className={styles.payprice}>
              实付款:￥123
            </span>
          </p>
        </div>

        <div className={styles.iteminfo} style={{ height: 'auto' }}>
          <Button type="warning" inline size="small">维修</Button>
        </div>
      </div>
    );
  }

}

export default WatchOrder;
