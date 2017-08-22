import React from 'react';

export default function button({ children, onClick, style }) {
  return (
    <div
      onClick={onClick}
      style={{
        background: '#FF5B55',
        color: '#ffffff',
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

