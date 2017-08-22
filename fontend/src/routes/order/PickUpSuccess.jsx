import React from 'react';
import { hashHistory } from 'dva/router';
import Button from '../../components/Button';
import styles from './index.less';

export default function PickUpSuccess() {
  return (
    <div className={styles.pickUpSuccess}>
      <div className={styles.titleContainer}>
        <p className={styles.title}>提车成功</p>
      </div>
      <div>
        <Button
          onClick={() => { hashHistory.replace('/'); }}
          style={{ width: '80%', margin: '0 auto' }}
        >
          查看订单
        </Button>
      </div>
    </div>
  );
}
