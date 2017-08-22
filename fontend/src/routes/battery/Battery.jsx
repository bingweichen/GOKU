import React, { Component } from 'react';
import { NoticeBar, Icon } from 'antd-mobile';
import styles from './index.less';

const functions = [
  { title: '扫一扫', icon: require('../../assets/image/QR-code.svg'), url: '', color: '#8BA6EE' },
  { title: '消费卡', icon: require('../../assets/image/card.svg'), url: '', color: '#FBBBB1' },
  { title: '闪充保修', icon: require('../../assets/image/fix.svg'), url: '', color: '#8FDBBE' },
];
class Battery extends Component {

  render() {
    return (
      <div>
        <NoticeBar mode="link" onClick={() => { }}>
          你正在使用闪充，还有5天剩余时间，点击归还！
        </NoticeBar>
        <div className={styles.functions}>
          {
            functions.map(value => (
              <div className={styles.function} style={{ background: value.color }}>
                <p><Icon type={value.icon} style={{ width: '.44rem', height: '.44rem' }} /></p>
                <p>{value.title}</p>
              </div>
            ))
          }
        </div>
      </div>
    );
  }
}

export default Battery;
