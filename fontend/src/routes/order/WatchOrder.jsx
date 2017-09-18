import React, { Component } from 'react';
import { Button } from 'antd-mobile';
import moment from 'moment';
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
    getOrder(this.state.orderId)
      .then(({ appointment }) => {
        this.setState({ order: appointment });
      });
  }

  render() {
    const { order } = this.state;
    let { price } = order.e_bike_model;
    price = (typeof price === 'number' ? price : price && price[order.rent_time_period]); // 为obj or number?
    const time = (order.end_time ?
      `${moment(order.date).format('YYYY年MM月DD日')}至${moment(order.end_time).format('YYYY年MM月DD日')}` : order.rent_time_period);
    return (
      <div className={styles.container}>
        <div className={styles.iteminfo}>
          <div style={{ width: '2rem', height: '2rem' }}>
            <img src={order.e_bike_model.image_urls[0]} alt="" style={{ maxWidth: '100%' }} />
          </div>
          <div className={styles.itemdec}>
            <p className={styles.name}>{order.e_bike_model.name}</p>
            <p className={styles.size}>{order.color}色,{order.type},{order.category}</p>
          </div>
        </div>

        <div className={styles.iteminfo} style={{ height: 'auto', display: order.type === '买车' ? 'none' : 'flex' }}>
          <p style={{ width: '2rem', margin: 0 }}>租用时间:</p>
          <p style={{ flex: 1, margin: 0, color: '#666666' }}>{time}</p>
        </div>

        <div className={styles.iteminfo} style={{ height: 'auto' }}>
          <p style={{ width: '2rem', margin: 0 }}>配送方式:</p>
          <p style={{ flex: 1, margin: 0, color: '#666666' }}>{order.delivery} </p>
        </div>

        <div className={styles.iteminfo} style={{ height: 'auto' }}>
          <p style={{ width: '2rem', margin: 0 }}>备注信息:</p>
          <p style={{ flex: 1, margin: 0, color: '#666666' }}>{order.note} </p>
        </div>

        <div className={styles.iteminfo} style={{ height: 'auto' }}>
          <p style={{ width: '2rem', margin: 0 }}>下单时间:</p>
          <p style={{ flex: 1, margin: 0, color: '#666666' }}>{new Date(order.date).toLocaleString()} </p>
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
              ￥{price}
            </span>
          </p>
          <p
            style={{
              color: '#333333',
              fontSize: '0.25rem',
              display: order.reduced_price === null ? 'none' : 'block',
            }}
          >
            <span >使用优惠卷:</span>
            <span style={{ float: 'right' }}>-￥{order.reduced_price}</span>
          </p>
          <p style={{ overflow: 'hidden' }}>
            <span className={styles.payprice}>
              实付款:￥{order.price}
            </span>
          </p>
        </div>

        {/* <div className={styles.iteminfo} style={{ height: 'auto' }}>
          <Button type="warning" inline size="small">维修</Button>
        </div> */}
      </div>
    );
  }

}

export default WatchOrder;
