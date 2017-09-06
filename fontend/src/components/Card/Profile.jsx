import React from 'react';
import LazyLoad from 'react-lazyload';
import { Link } from 'dva/router';
import styles from './Profile.less';

export default function Profile({ car }) {
  const { image_urls, name, price, num_view } = car;
  let carPrice = price;
  if (typeof price === 'object') { // 租车
    carPrice = '';
    for (const p in price) {
      if (Object.prototype.hasOwnProperty.call(price, p)) {
        carPrice = `${carPrice}${price[p]}/${p} `;
      }
    }
  }
  return (
    <div style={{ background: '#ffffff' }}>
      <Link to={{ pathname: `cardetail/${name}` }}>
        <div className={styles.container}>
          <LazyLoad height={300}>
            <img src={image_urls && image_urls[0]} alt="" className={styles.image} />
          </LazyLoad>
        </div>
        <div className={styles.footer}>
          <p className={styles.title}>{name}</p>
          <p className={styles.price}>￥{carPrice}</p>
          <p className={styles.visited}>浏览量:{num_view}</p>
        </div>
      </Link>
    </div>
  );
}

Profile.prototype = {

};

