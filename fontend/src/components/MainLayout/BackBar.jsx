// 右上角返回
import React from 'react';
import { Icon } from 'antd-mobile';
import { hashHistory } from 'dva/router';
import PropTypes from 'prop-types';

export default function BackBar({ backpage, pathname }) {
  return (
    <div style={{ height: '.6rem', lineHeight: '.6rem' }}>
      <Icon
        style={{ height: '.6rem' }}
        type="left"
      />
      <span
        style={{ fontSize: '.32rem', width: '.6rem', verticalAlign: 'top' }}
        onClick={() => {
          if (pathname) {
            hashHistory.push({ pathname });
          } else {
            hashHistory.goBack();
          }
        }}
      >
        {backpage || '返回'}
      </span>
    </div>
  );
}

BackBar.propType = {
  backpage: PropTypes.string,
  pathname: PropTypes.string,
};
