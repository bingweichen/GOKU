import React from 'react';
import { hashHistory } from 'dva/router';
import styles from './item.less';
import { orderStatus } from '../../utils/constant.js';

export default function Item({ order }) {
  return (
    <div className={styles.item}>
      <div
        style={{ display: 'flex' }}
        onClick={() => { hashHistory.push(`/watchorder?id=${order.id}`); }}
      >
        <div className={styles.imgContainer}>
          <img
            style={{ maxWidth: '100%' }}
            src={order.e_bike_model.image_urls[0]} alt=""
          />
        </div>
        <div className={styles.info}>
          <p className={styles.name}>{order.e_bike_model.name}</p>
          <p className={styles.detail}>{order.color}色，{order.delivery}</p>
          <p className={styles.detail}>订单时间:{new Date(order.date).toLocaleString()}</p>
        </div>
      </div>
      <p className={styles.status}>{order.status}</p>
      {/* 待收货 */}
      <div className={styles.operate}>
        <div
          style={{
            color: '#FF5B55',
            border: '1px solid #FF5B55',
          }}
          className={styles.contact}
        >
          <span style={{ display: order.status === orderStatus.waitPayAppointment ? 'inline' : 'none' }}>去支付</span>
          <span
            onClick={() => { hashHistory.push(`/pickupcar?id=${order.id}`); }}
            style={{ display: order.status === orderStatus.waitPickUp ? 'inline' : 'none' }}
          >去提车</span>
          <span
            style={{ display: order.status === orderStatus.finish ? 'inline' : 'none' }}
          >报修</span>
        </div>
        {/* <div
          style={{
            display: order.status === orderStatus.waitPayAppointment ? 'block' : 'none',
            color: '#FF5B55',
            border: '1px solid #FF5B55',
          }}
          className={styles.contact}
        >
          <span>提车</span>
        </div> */}
        {/* 待归还 */}
        {/* <div
          style={{
            display: order.status === orderStatus.waitPickUp ? 'block' : 'none',
            color: '#FF5B55',
            border: '1px solid #FF5B55',
          }}
          className={styles.contact}
        >
          <span>报修</span>
        </div> */}
        {/* <div className={styles.contact}>
          <span>联系客服</span>
        </div> */}
      </div>
    </div >
  );
}
