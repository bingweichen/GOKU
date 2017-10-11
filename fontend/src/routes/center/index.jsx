// 个人中心的首页
import React, { Component } from 'react';
import { hashHistory } from 'dva/router';
import { List, Button } from 'antd-mobile';
import { connect } from 'dva';
import styles from './index.less';
import Coupons from './Coupons';
import Signup from './Signup';
import Signin from './Signin';
import { getVirtualCard, openVirtualCardService } from '../../services/battery.js';
import UserInfo from './UserInfo';

const Item = List.Item;

const logout = () => {
  localStorage.removeItem('token');
  hashHistory.push('/signin');
};

class Center extends Component {
  async handleClickVirtualCard() {
    this.setState({ isloading: true });
    try {
      const { balance, deposit } = await getVirtualCard();
      this.props.updateCount({
        balance,
        deposit,
      });
      hashHistory.push('/balance');
    } catch (error) {
      if (error.status === 400) {
        alert(error.message.message, '确定开通吗？', [
          { text: '取消', style: 'default' },
          { text: '确定', onPress: () => openVirtualCardService() },
        ]);
      }
      this.setState({ isloading: false });
    }
  }

  render() {
    return (
      <div>
        <div className={styles.cover}>
          <div className={styles.userPhoto}>
            <img src={sessionStorage.getItem('head')} alt="" style={{ width: '100%' }} />
          </div>
        </div>
        <p className={styles.username}>{localStorage.getItem('username')}</p>
        <List>
          <Item
            onClick={() => hashHistory.push('/userinfo')}
            thumb="https://zos.alipayobjects.com/rmsportal/dNuvNrtqUztHCwM.png"
            arrow="horizontal"
          >个人信息</Item>
          <Item
            thumb="https://zos.alipayobjects.com/rmsportal/UmbJMbWOejVOpxe.png"
            arrow="horizontal"
            onClick={() => { hashHistory.push('/coupons'); }}
          >我的优惠券</Item>
          <Item
            thumb="https://zos.alipayobjects.com/rmsportal/dNuvNrtqUztHCwM.png"
            arrow="horizontal"
            onClick={() => { this.handleClickVirtualCard(); }}
          >虚拟消费卡</Item>
        </List>
        <Button
          onClick={logout}
          type="warning"
          className={styles.logout}
        > 退出登录 </Button>
      </div>
    );
  }
}

const mapStateToProps = (state) => {
  const { battery } = state;
  return {
    useDate: battery.inuseBattery && battery.inuseBattery.useDate, // 正在使用的电动车
    number: battery.inuseBattery && battery.inuseBattery.number,
  };
};

const mapDispatchToProps = (dispatch) => {
  return {
    updateCount: (account) => { dispatch({ type: 'battery/updateCount', ...account }); },
    getInuseBattery: () => { dispatch({ type: 'battery/getInuseBattery' }); },
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Center);
export {
  Coupons,
  Signup,
  Signin,
  UserInfo,
};
