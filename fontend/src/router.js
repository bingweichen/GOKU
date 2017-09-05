import React from 'react';
import { Router, Route } from 'dva/router';
import IndexPage from './routes/IndexPage';
import CarDetail from './routes/shop/CarDetail.jsx';
import OrderSuccess from './routes/shop/OrderSuccess.jsx';
import OrderDetail from './routes/order/OrderDetail.jsx';
import PickUpSite from './routes/custom/PickUpSite.jsx';
import Order, {
  PickUpCar,
  PickUpSuccess,
  WatchOrder,
  Reparis,
} from './routes/order';
import {
  Balance,
  ExpenseRecord,
  UseBattery,
} from './routes/battery';
import {
  Coupons,
  Signup,
  Signin,
} from './routes/center';

function RouterConfig({ history }) {
  return (
    <Router history={history}>
      <Route path="/" component={IndexPage} />
      <Route path="/cardetail/:id" component={CarDetail} />
      <Route path="/ordersuccess" component={OrderSuccess} />
      <Route path="/orderdetail" component={OrderDetail} />
      <Route path="/pickupsite" component={PickUpSite} />
      <Route path="/order" component={Order} />
      <Route path="/pickupcar" component={PickUpCar} />
      <Route path="/balance" component={Balance} />
      <Route path="/expenserecord" component={ExpenseRecord} />
      <Route path="/usebattery" component={UseBattery} />
      <Route path="/coupons" component={Coupons} />
      <Route path="/signup" component={Signup} />
      <Route path="/signin" component={Signin} />
      <Route path="/pickupsuccess" component={PickUpSuccess} />
      <Route path="/watchorder" component={WatchOrder} />
      <Route path="/repairs" component={Reparis} />
    </Router>
  );
}

export default RouterConfig;
