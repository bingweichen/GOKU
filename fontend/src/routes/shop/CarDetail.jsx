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

  handClickOrder = (type) => {
    if (this.state.color === '') {
      Toast.info('请先选择颜色!!!');
      return;
    }
    const buyType = (type === '租车') ? 'rent' : 'buy';
    hashHistory.push({
      pathname: `/orderdetail?type=${buyType}&&carType=${this.props.name}&&color=${this.state.color}`,
    });
  }

  render() {
    const { image_urls, name, price, num_view, colors, introduction_image_urls, type } = this.props;
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
            <span className={styles.price}>
              ￥{typeof price === 'number' ? price : `${price['学期']}/学期,￥${price['年']}/年`}
            </span>
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
          {
            introduction_image_urls.map(img => (
              <img src={img} alt="" style={{ width: '100%', minHeight: '1rem' }} key={img} />
            ))
          }
        </div>
        <Footer
          title="去预约"
          onClick={
            () => { this.handClickOrder(type); }
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
