import React from 'react';
import Button from '../../components/Button';
import styles from './index.less';

export default function UseBattery() {
  return (
    <div className={styles.usebattery}>
      <div className={styles.batterInfo}>
        <p><span>闪充编号</span></p>
        <p>123456</p>
      </div>
      <div className={styles.useMessage}>
        <Button style={{ width: '100%' }}>确认使用</Button>
        <p>未交押金，无法享受闪充服务
          <span style={{ color: '#FF5B55' }}> 去充值</span>
        </p>
      </div>
    </div>
  );
}
