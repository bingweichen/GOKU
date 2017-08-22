import React from 'react';
import { Carousel, Icon } from 'antd-mobile';
import PropTypes from 'prop-types';
import { Link } from 'dva/router';
import styles from './index.less';

export default function CarCaroursel({ images }) {
  if (typeof images === 'string') {
    images = [images];
  }
  return (
    <div style={{ height: '7.5rem' }}>
      <Link to="/">
        <div className={styles.back}>
          <Icon type="left" className={styles.backIcon} />
        </div>
      </Link>
      <Carousel style={{ height: '7.5rem' }}>
        {
          images.map(image => (
            <a style={{ width: '100%', height: '7.5rem' }} key={image}>
              <img src={image} alt="" style={{ width: '100%', height: '7.5rem' }} />
            </a>
          ))
        }
      </Carousel>
    </div>
  );
}

CarCaroursel.protoTypes = {
  images: PropTypes.array,
};
