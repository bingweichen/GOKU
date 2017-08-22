import React from 'react';

export default function StepInput({ setValue, value, style }) {
  const arr = [0, 1, 2, 3, 4, 5];
  return (
    <div style={{ position: 'relative', ...style }}>
      <input
        style={{
          width: '100%',
          height: '100%',
          position: 'absolute',
          opacity: '0',
        }}
        maxLength="6" onChange={(e) => { setValue(e.target.value); }}
      />
      <div style={{ display: 'flex' }}>
        {
          arr.map(i => (
            <div
              style={{
                border: '1px solid #000000',
                height: '0.9rem',
                flex: 1,
                textAlign: 'center',
                lineHeight: '.9rem',
                fontSize: '.6rem',
              }}
              key={i}
            >
              {value[i]}
            </div>
          ))
        }
      </div>
    </div >
  );
}

