import React from 'react';
import Item from './Item';

export default function WaitExtract({ orders }) {
  return (
    <div>
      {
        orders.map((order) => {
          return (
            <Item order={order} key={order.id} />
          );
        })
      }
    </div>
  );
}
