import React, { Component } from 'react';
import { connect } from 'dva';
import { hashHistory } from 'dva/router';
import { Layout, Icon, Menu, Button } from 'antd';
import styles from './Admin.less';

const { SubMenu } = Menu;
const { Header, Content, Sider } = Layout;
// 退出
function logout() {
  localStorage.removeItem('token');
  hashHistory.push('/sign');
}

class Admin extends Component {
  state = {
    collapsed: false,
  };

  toggle = () => {
    this.setState({
      collapsed: !this.state.collapsed,
    });
  }

  render() {
    const siders = [
      { icon: 'user', key: 'order', title: '订单' },
      { icon: 'user', key: 'car', title: '车辆信息' },
      { icon: 'user', key: 'user', title: '用户信息' },
      { icon: 'user', key: 'storage', title: '库存管理' },
      { icon: 'user', key: 'setting', title: '参数设置' },
      { icon: 'user', key: 'coupons', title: '优惠卷' },
      { icon: 'user', key: 'store', title: '商铺管理' },
      { icon: 'user', key: 'school', title: '学校管理' },
      { icon: 'user', key: 'NO', title: '编号管理' },
      // { icon: 'user', key: 'battery', title: '电池管理' },
      { icon: 'user', key: 'report', title: '保修' },
      { icon: 'user', key: 'refund', title: '退款' },
      { icon: 'user', key: 'person', title: '个人中心' },
    ];
    return (
      <div>
        <Layout>
          <Sider
            trigger={null}
            collapsible
            collapsed={this.state.collapsed}
          >
            <div className={styles.logo} />
            <Menu
              onSelect={({ key }) => { hashHistory.push(`/admin/${key}`); }}
              theme="dark"
              mode="inline"
              defaultSelectedKeys={['order']}
            >
              {
                siders.map(sider => (
                  <Menu.Item key={sider.key}>
                    <Icon type={sider.icon} />
                    <span>{sider.title}</span>
                  </Menu.Item>
                ))
              }
              <SubMenu key="battery" title={<span><Icon type="setting" /><span>电池管理</span></span>}>
                <Menu.Item key="battery">电池</Menu.Item>
                <Menu.Item key="battery/record">电池记录</Menu.Item>
                <Menu.Item key="battery/report">电池报修</Menu.Item>
              </SubMenu>
            </Menu>
          </Sider>
          <Layout>
            <Header style={{ background: '#fff', padding: 0 }}>
              <Icon
                className={styles.trigger}
                type={this.state.collapsed ? 'menu-unfold' : 'menu-fold'}
                onClick={this.toggle}
              />
              <Button
                onClick={logout}
                style={{ float: 'right', marginTop: 18 }}
              >
                退出<Icon type="logout" />
              </Button>
            </Header>
            <Content style={{ margin: '24px 16px', padding: 24, background: '#fff', minHeight: 1000 }}>
              {this.props.children}
            </Content>
          </Layout>
        </Layout>
      </div>

    );
  }
}

function mapStateToProps() {
  return {};
}

export default connect(mapStateToProps)(Admin);
