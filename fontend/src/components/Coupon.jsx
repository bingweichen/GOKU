// 单个优惠券
import React from 'react';
import styles from './styles/Coupon.less';

export default function Coupon({ desc, expired, value }) {
  return (
    <div className={styles.coupon}>
      <div className={styles.left}>
        <p>
          <span>抵用卷</span>
          <span className={styles.desc}>{desc}</span>
        </p>
        <p>
          <span className={styles.time}>过期时间：{expired}</span>
        </p>
      </div>
      <div className={styles.right}>
        ￥{value}
      </div>
      <div className={styles.top} />
      <div className={styles.bottom} />
    </div>
  );
}
