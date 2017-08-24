import React, { Component } from 'react';
import moment from 'moment';
import { ActivityIndicator } from 'antd-mobile';
import { moneyType } from '../../utils/constant.js';
import styles from './index.less';
import { record } from '../../services/battery.js';

class ExpenseRecord extends Component {

  state = {
    orders: [],
    isloading: true,
  }

  componentDidMount() {
    record()
      .then((orders) => {
        const arr = orders.map((order) => {
          return {
            type: order.consume_event,
            money: order.consume_fee,
            time: new Date(order.consume_date_time),
            id: order.id,
          };
        });
        arr.sort((a, b) => b.id - a.id);
        this.setState({ orders: arr });
      })
      .finally(() => {
        this.setState({ isloading: false });
      });
  }

  render() {
    return (
      <div className={styles.ExpenseRecord}>
        {
          this.state.orders.map((order) => {
            return (
              <div className={styles.item} key={order.id}>
                <p>
                  <span>{moneyType[order.type]}</span>
                </p>
                <p>
                  <span style={{ fontSize: '.24rem' }}>
                    <span
                      style={{
                        color: '#333333',
                        fontSize: '.24rem',
                      }}
                    >
                      {moment(order.time).format('YYYY-MM-DD HH:mm')}</span>
                  </span>
                  <span>{order.money}元</span>
                </p>
              </div>
            );
          })
        }
        <ActivityIndicator
          toast
          text="加载中"
          animating={this.state.isloading}
        />
      </div>
    );
  }
}

export default ExpenseRecord;
