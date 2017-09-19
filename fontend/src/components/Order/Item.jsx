import React from 'react';
import { hashHistory } from 'dva/router';
import { Toast, Modal } from 'antd-mobile';
import axios from '../../utils/axios.js';
import styles from './item.less';
import { orderStatus } from '../../utils/constant.js';
import { wxpay } from '../../wechat';

const { alert } = Modal;
export default function Item({ order }) {
  const { status } = order;
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
          <p className={styles.detail}>订单编号:{order.id}</p>
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
          {/* 代付预约款 */}
          <span
            onClick={() => {
              // todo wechat pay
              axios.post('appointment/status/appointment_payment_success', {
                appointment_id: order.id,
                openid: localStorage.openid,
              }).then(data => wxpay(data, () => { hashHistory.push(`/watchorder?id=${order.id}`); }));
            }}
            style={{ display: order.status === orderStatus.waitPayAppointment ? 'inline' : 'none' }
            }>去支付</span>
          {/* 取消的订单  */}
          <span style={{ display: order.status === orderStatus.cancel ? 'inline' : 'none' }}>订单已取消</span>
          <span
            onClick={() => {
              alert('你需要去店里进行还车', '请前往店内还车', [
                { text: '确定' },
              ]);
            }}
            style={{ display: order.status === orderStatus.waitBack ? 'inline' : 'none' }}
          >去还车</span>
          <span
            onClick={() => { hashHistory.push(`/pickupcar?id=${order.id}`); }}
            style={{ display: order.status === orderStatus.waitPickUp ? 'inline' : 'none' }}
          >去提车</span>
          <span
            style={{ display: order.status === orderStatus.finish ? 'inline' : 'none' }}
            onClick={() => { hashHistory.push(`/repairs?id=${order.id}`); }}
          >报修</span>
        </div>
        {/* 取消订单 */}
        <div
          onClick={() => {
            alert('取消订单', '确定取消吗?', [
              { text: '取消', onPress: () => console.log('cancel') },
              {
                text: '确定',
                onPress: () => {
                  axios.post('appointment/status/cancel', {
                    appointment_id: order.id,
                  }).then(() => {
                    Toast.success('取消成功', 0.5, () => { location.reload(); });
                  });
                },
              },
            ]);
          }}
          style={{
            display: (status === orderStatus.waitPayAppointment ||
              status === orderStatus.waitPickUp
            ) ? 'block' : 'none',
            color: '#FF5B55',
            border: '1px solid #FF5B55',
          }}
          className={styles.contact}
        >
          <span>取消订单</span>
        </div>
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
