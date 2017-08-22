import React from 'react';
import { Link } from 'dva/router';
import styles from './OrderSuccess.less';

export default function OrderSuccess() {
  return (
    <div>
      <div className={styles.top}>
        <p className={styles.success}>预约成功</p>
        <p className={styles.watchorder}>查看订单</p>
        <p className={styles.other}>
          <span className={styles.contact}>联系客服</span>
          <Link to="/pickupsite">
            <span className={styles.pickup}>
              查看自提点
          </span>
          </Link>
        </p>
      </div>
      <div className={styles.bottom}>
        <p className={styles.warning}>注意</p>
        <p>·本次预约一周内有效，且一周内只能预约一次，逾期需另行预约。</p>
        <p>·自提请携带身份证到线下店铺进行提车。</p>
      </div>
    </div>
  );
}
