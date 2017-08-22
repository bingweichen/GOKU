import React, { Component } from 'react';
import { hashHistory } from 'dva/router';
import { List } from 'antd-mobile';
import styles from './index.less';
import Coupons from './Coupons';
import Signup from './Signup';
import Signin from './Signin';

const Item = List.Item;
class Center extends Component {
  render() {
    return (
      <div>
        <div className={styles.cover}>
          <div className={styles.userPhoto}>
            <img src="https://gw.alicdn.com/sns_logo/i4/6000000003878/TB2QR08uZtnpuFjSZFKXXalFFXa_!!0-mytaobao.jpg" alt="" />
          </div>
        </div>
        <p className={styles.username}>包泽峰</p>
        <List>
          <Item
            thumb="https://zos.alipayobjects.com/rmsportal/dNuvNrtqUztHCwM.png"
            arrow="horizontal"
          >个人信息</Item>
          <Item
            thumb="https://zos.alipayobjects.com/rmsportal/UmbJMbWOejVOpxe.png"
            arrow="horizontal"
            onClick={() => { hashHistory.push('/coupons'); }}
          >我的优惠卷</Item>
        </List>
      </div>
    );
  }
}

export default Center;
export {
  Coupons,
  Signup,
  Signin,
};
