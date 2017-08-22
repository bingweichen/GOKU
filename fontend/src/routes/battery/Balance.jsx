import React, { Component } from 'react';
import Button from '../../components/Button';
import styles from './index.less';

class Balance extends Component {
  render() {
    return (
      <div style={{ padding: '0 .5rem' }}>
        <div className={styles.money}>
          <p style={{ fontSize: '.28rem' }}>账户余额(元)</p>
          <p style={{ fontSize: '1.2rem', margin: 0 }}>18</p>
        </div>
        <Button style={{ width: '100%' }}>充值</Button>
        <Button style={{ width: '100%', marginTop: '.5rem' }}>消费记录</Button>
        <div>
          <p style={{ textAlign: 'center', fontSize: '.28rem' }}>
            <span style={{ color: '#616060' }}>押金199元</span>
            <a style={{ color: 'rgb(255, 91, 85)', marginLeft: '.28rem' }}>退还押金</a>
          </p>
        </div>
      </div >
    );
  }
}

export default Balance;

