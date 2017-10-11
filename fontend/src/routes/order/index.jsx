// 订单的首页
import React, { Component } from 'react';
import { Tabs } from 'antd-mobile';
import { connect } from 'dva';
import { WaitExtract } from '../../components/Order';
import styles from './index.less';
import PickUpCar from './PickUpCar';
import PickUpSuccess from './PickUpSuccess';
import WatchOrder from './WatchOrder';
import Reparis from './Reparis';
import { orderStatus } from '../../utils/constant.js';

const TabPane = Tabs.TabPane;
class Order extends Component {

  state = {
    active: 0,
  }

  componentDidMount() {
    this.props.getData();
  }

  render() {
    const { orders } = this.props;
    return (
      <div style={{ paddingBottom: '1rem' }}>
        <Tabs defaultActiveKey="0" swipeable={false}>
          <TabPane tab="全部" key="0">
            <div style={{ alignItems: 'center', backgroundColor: '#fff' }}>
              <WaitExtract type="0" orders={orders} />
            </div>
          </TabPane>
          <TabPane tab="待提货" key="1">
            <div style={{ alignItems: 'center', backgroundColor: '#fff' }}>
              <WaitExtract type="1" orders={orders.filter(order => order.status === orderStatus.waitPickUp)} />
            </div>
          </TabPane>
          <TabPane tab="待归还" key="2">
            <div style={{ alignItems: 'center', backgroundColor: '#fff' }}>
              <WaitExtract type="2" orders={orders.filter(order => order.status === orderStatus.waitBack)} />
            </div>
          </TabPane>
          <TabPane tab="已完成" key="3">
            <div style={{ alignItems: 'center', backgroundColor: '#fff' }}>
              <WaitExtract type="3" orders={orders.filter(order => order.status === orderStatus.finish)} />
            </div>
          </TabPane>
        </Tabs>
      </div>
    );
  }
}

const mapStateToProps = (state) => {
  const { person } = state;
  return {
    orders: person.orders,
  };
};

export default connect(mapStateToProps)(Order);
export {
  PickUpCar,
  PickUpSuccess,
  WatchOrder,
  Reparis,
};
