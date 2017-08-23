import React from 'react';
import { TabBar, Icon } from 'antd-mobile';
import { hashHistory } from 'dva/router';
import PropTypes from 'prop-types';
import { connect } from 'dva';
import Shop from '../../routes/shop';
import Order from '../../routes/order';
import Center from '../../routes/center';
import Battery from '../../routes/battery';

class Footer extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedTab: props.tab,
      hidden: false,
    };
  }

  render() {
    return (
      <TabBar
        unselectedTintColor="#949494"
        tintColor="#33A3F4"
        barTintColor="white"
        hidden={this.state.hidden}
      >
        <TabBar.Item
          title="商城"
          key="shop"
          icon={<div
            style={{
              width: '0.44rem',
              height: '0.44rem',
              background: 'url(https://zos.alipayobjects.com/rmsportal/sifuoDUQdAFKAVcFGROC.svg) center center /  0.42rem 0.42rem no-repeat',
            }}
          />
          }
          selectedIcon={<div
            style={{
              width: '0.44rem',
              height: '0.44rem',
              background: 'url(https://zos.alipayobjects.com/rmsportal/iSrlOTqrKddqbOmlvUfq.svg) center center /  0.42rem 0.42rem no-repeat',
            }}
          />
          }
          selected={this.props.tab === 'shop'}
          onPress={() => {
            hashHistory.replace('/?tab=shop');
          }}
          data-seed="logId"
        >
          <Shop />
        </TabBar.Item>
        <TabBar.Item
          icon={<Icon type="koubei-o" size="md" />}
          selectedIcon={<Icon type="koubei" size="md" />}
          title="闪充"
          key="闪充"
          selected={this.props.tab === 'flash'}
          onPress={() => {
            hashHistory.replace('/?tab=flash');
          }}
          data-seed="logId1"
        >
          <Battery />
        </TabBar.Item>
        <TabBar.Item
          icon={
            <div
              style={{
                width: '0.44rem',
                height: '0.44rem',
                background: 'url(https://zos.alipayobjects.com/rmsportal/psUFoAMjkCcjqtUCNPxB.svg) center center /  0.42rem 0.42rem no-repeat'
              }}
            />
          }
          selectedIcon={
            <div
              style={{
                width: '0.44rem',
                height: '0.44rem',
                background: 'url(https://zos.alipayobjects.com/rmsportal/IIRLrXXrFAhXVdhMWgUI.svg) center center /  0.42rem 0.42rem no-repeat'
              }}
            />
          }
          title="订单"
          key="订单"
          selected={this.props.tab === 'order'}
          onPress={() => {
            this.props.getOrder();
            hashHistory.replace('/?tab=order');
          }}
        >
          <Order />
        </TabBar.Item>
        <TabBar.Item
          icon={{ uri: 'https://zos.alipayobjects.com/rmsportal/asJMfBrNqpMMlVpeInPQ.svg' }}
          selectedIcon={{ uri: 'https://zos.alipayobjects.com/rmsportal/gjpzzcrPMkhfEqgbYvmN.svg' }}
          title="我的"
          key="我的"
          selected={this.props.tab === 'center'}
          onPress={() => {
            hashHistory.replace('/?tab=center');
          }}
        >
          <Center />
        </TabBar.Item>
      </TabBar>
    );
  }
}
const mapStateToProps = () => {
  return {};
};

const mapDispatchToProps = (dispatch) => {
  return {
    getOrder: () => { dispatch({ type: 'person/getOrder' }); },
  };
};

Footer.PropTypes = {
  tab: PropTypes.string,
};

export default connect(mapStateToProps, mapDispatchToProps)(Footer);
