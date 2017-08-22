import React, { Component } from 'react';
import { connect } from 'dva';
import { hashHistory } from 'dva/router';
import { Picker, List, Toast } from 'antd-mobile';
import CarCarousel from '../../components/CarDetail/CarCarousel';
import styles from './CarDetail.less';
import Footer from '../../components/CarDetail/BuyFooter';

class CarDetail extends Component {

  state = {
    color: '',
  }

  handClickOrder = (type, carType) => {
    if (this.state.color === '') {
      Toast.info('请先选择颜色!!!');
      return;
    }
    hashHistory.push({
      pathname: `/orderdetail?type=${type}&&carType=${this.props.name}&&color=${this.state.color}`,
    });
  }

  render() {
    const { image_urls, name, price, num_view, colors } = this.props;
    const carColors = colors.map(color => ({
      value: color,
      label: color,
    }));
    return (
      <div>
        <CarCarousel images={image_urls} />
        <div className={styles.header}>
          <p className={styles.title}>{name}</p>
          <p style={{ marginBottom: 0 }}>
            <span className={styles.price}>￥{price}</span>
            <span className={styles.visited}>{num_view}浏览</span>
          </p>
        </div>
        <div style={{ padding: '14px 0px' }}>
          <Picker
            onChange={(color) => { this.setState({ color }); }}
            data={carColors}
            cols={1}
            value={this.state.color}
          >
            <List.Item arrow="horizontal" style={{ fontSize: '0.2rem' }}>选择颜色</List.Item>
          </Picker>
        </div>
        <div>
          <img src="https://img10.360buyimg.com/cms/jfs/t3490/20/841716619/331496/a8a0c938/5819a2a2N0ad6bc8a.jpg" alt="" style={{ width: '100%' }} />
        </div>
        <Footer
          title="去预约"
          onClick={
            () => { this.handClickOrder('buy'); }
          }
        />
      </div>
    );
  }
}

const mapStateToProps = (state) => {
  return state.shop;
};

export default connect(mapStateToProps)(CarDetail);
