import React from 'react';
import styles from './index.less';

export default function ExpenseRecord() {
  return (
    <div className={styles.ExpenseRecord}>
      <div className={styles.item}>
        <p>
          <span>在线充值</span>
          <span
            style={{
              color: '#333333',
              fontSize: '.24rem',
            }}
          >
            2017-01-01</span>
        </p>
        <p>
          <span style={{ fontSize: '.24rem' }}>余额（元）：400</span>
          <span>+400.00</span>
        </p>
      </div>
    </div>
  );
}
