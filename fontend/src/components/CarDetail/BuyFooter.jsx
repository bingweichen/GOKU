import React from 'react';
import { Icon } from 'antd-mobile';
import styles from './index.less';

export default function BuyFooter({ onClick, title }) {
  return (
    <div className={styles.footer}>
      <div className={styles.service}>
        <p><Icon type={require('../../assets/image/service.svg')} /></p>
        <p>联系客服</p>
      </div>
      {/* <div className={styles.item} style={{ background: '#ff9402', opacity: 0 }}>
        <span>立即购买</span>
      </div> */}
      <div className={styles.item} style={{ background: '#ff5000' }} onClick={onClick}>
        <span>{title}</span>
      </div>
    </div>
  );
}
