import React from 'react';
import { connect } from 'dva';
import Coupon from '../../components/Coupon';

// 优惠卷页面
function Coupons({ coupons }) {
  if (coupons.length === 0) {
    return (
      <div
        style={{
          textAlign: 'center',
          color: '#615965',
          height: '6rem',
          lineHeight: '6rem',
        }}
      >
        <span>暂无优惠卷!</span>
      </div>
    );
  }
  return (
    <div style={{ padding: '.3rem', background: '#ffffff' }}>
      {
        coupons.map(coupon => (
          <Coupon
            key={coupon.id}
            desc={coupon.desc}
            value={coupon.value}
            expired={new Date(coupon.expired).toLocaleString()}
          />
        ))
      }
    </div>
  );
}

const mapStateToProps = (state) => {
  const { person } = state;
  return {
    coupons: person.coupons,
  };
};

export default connect(mapStateToProps)(Coupons);
