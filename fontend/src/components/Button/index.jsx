// 自定义的按钮组件
import React from 'react';
import PropTypes from 'prop-types';

export default function button({ children, onClick, style, active }) {
  return (
    <div
      onClick={onClick}
      style={{
        background: '#FF5B55',
        color: active ? '#C5C5C5' : '#ffffff',
        width: '2.5rem',
        height: '.6rem',
        textAlign: 'center',
        borderRadius: '.36rem',
        lineHeight: '.6rem',
        ...style,
      }}
    >
      <span>{children}</span>
    </div>
  );
}

button.PropTypes = {
  chilren: PropTypes.string,
  onClick: PropTypes.func,
  style: PropTypes.object,
  active: PropTypes.bool,
};
