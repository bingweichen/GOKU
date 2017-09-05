import React from 'react';
import Item from './Item';

export default function WaitExtract({ orders }) {
  return (
    <div>
      {
        orders.sort((a, b) => b.id - a.id).map((order) => {
          return (
            <Item order={order} key={order.id} />
          );
        })
      }
    </div>
  );
}
