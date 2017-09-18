import React, { Component } from 'react';
import { Icon, SearchBar, Flex, Popover } from 'antd-mobile';
import PropTypes from 'prop-types';
import styles from './Header.css';

const FlexItem = Flex.Item;
const PopoverItem = Popover.Item;
class Header extends Component {

  state = {
    visible: false,
    inSearch: false,
  };

  handleVisibleChange = (visible) => {
    this.setState({
      visible,
    });
  };

  render() {
    const carTypes = ['小龟', '酷车', 'MINI租', '闪租'];
    return (
      <Flex className={styles.header}>
        <FlexItem style={{ width: '1.5rem', flex: 'none', display: this.state.inSearch ? 'none' : 'flex' }}>
          <Popover
            mask
            overlayStyle={{ color: 'currentColor' }}
            visible={this.state.visible}
            overlay={[
              (<PopoverItem key="1" value="小龟">小龟</PopoverItem>),
              (<PopoverItem key="2" value="酷车" style={{ whiteSpace: 'nowrap' }}>酷车</PopoverItem>),
              (<PopoverItem key="3" value="MINI租" >
                <span style={{ marginRight: 5 }}>MINI租</span>
              </PopoverItem>),
              (<PopoverItem key="4" value="闪租">闪租</PopoverItem>),
            ]}
            onVisibleChange={this.handleVisibleChange}
            onSelect={(x, index) => {
              this.props.changeCarType(carTypes[index]);
              this.setState({ visible: false });
            }}
            placement="bottomLeft"
          >
            <div
              style={{
                height: '100%',
                padding: '0 0 0 0.1rem',
                display: 'flex',
                alignItems: 'center',
                fontSize: '.3rem',
              }}
            >
              <Icon type="down" />{this.props.carType}
            </div>
          </Popover>
        </FlexItem>
        <FlexItem style={{ marginLeft: '1.16rem' }}>
          GOKU·出行
        </FlexItem>
        {/* <FlexItem>
          <SearchBar
            onFocus={() => { this.setState({ inSearch: true }); }}
            onBlur={() => { this.setState({ inSearch: false }); }}
            placeholder="搜索"
          />
        </FlexItem>
        <FlexItem style={{ flex: 'none', margin: '0 0.1rem 0 0', display: this.state.inSearch ? 'none' : 'flex' }}>
          <Icon type={require('../../assets/image/message.svg')} />
        </FlexItem> */}
      </Flex >
    );
  }
}

export default Header;

Header.protoType = {
  carType: PropTypes.string,
};
