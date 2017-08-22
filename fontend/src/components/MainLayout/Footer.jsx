import React from 'react';
import { TabBar, Icon } from 'antd-mobile';
import { connect } from 'dva';
import Shop from '../../routes/shop';
import Order from '../../routes/order';
import Center from '../../routes/center';
import Battery from '../../routes/battery';

class Footer extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedTab: 'order',
      hidden: false,
    };
  }

  // renderContent(pageText) {
  //   return (
  //     <div style={{ backgroundColor: 'white', height: '100%', textAlign: 'center' }}>
  //       <div style={{ paddingTop: 60 }}>你已点击“{pageText}” tab， 当前展示“{pageText}”信息</div>
  //       <a
  //         style={{ display: 'block', marginTop: 40, marginBottom: 600, color: '#108ee9' }}
  //         onClick={(e) => {
  //           e.preventDefault();
  //           this.setState({
  //             hidden: !this.state.hidden,
  //           });
  //         }}
  //       >
  //         点击切换 tab-bar 显示/隐藏
  //       </a>
  //     </div>
  //   );
  // }

  render() {
    return (
      <TabBar
        unselectedTintColor="#949494"
        tintColor="#33A3F4"
        barTintColor="white"
        hidden={this.state.hidden}
      >
        <TabBar.Item
          title="生活"
          key="生活"
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
          selected={this.state.selectedTab === 'blueTab'}
          onPress={() => {
            this.setState({
              selectedTab: 'blueTab',
            });
          }}
          data-seed="logId"
        >
          <Shop />
        </TabBar.Item>
        <TabBar.Item
          icon={<Icon type="koubei-o" size="md" />}
          selectedIcon={<Icon type="koubei" size="md" />}
          title="口碑"
          key="口碑"
          badge={'new'}
          selected={this.state.selectedTab === 'redTab'}
          onPress={() => {
            this.setState({
              selectedTab: 'redTab',
            });
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
          selected={this.state.selectedTab === 'order'}
          onPress={() => {
            this.props.getOrder();
            this.setState({
              selectedTab: 'order',
            });
          }}
        >
          <Order />
        </TabBar.Item>
        <TabBar.Item
          icon={{ uri: 'https://zos.alipayobjects.com/rmsportal/asJMfBrNqpMMlVpeInPQ.svg' }}
          selectedIcon={{ uri: 'https://zos.alipayobjects.com/rmsportal/gjpzzcrPMkhfEqgbYvmN.svg' }}
          title="我的"
          key="我的"
          selected={this.state.selectedTab === 'yellowTab'}
          onPress={() => {
            this.setState({
              selectedTab: 'yellowTab',
            });
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

export default connect(mapStateToProps, mapDispatchToProps)(Footer);
