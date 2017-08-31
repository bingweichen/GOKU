import React from 'react';
import { Router } from 'dva/router';

const cached = {};
function registerModel(app, model) {
  if (!cached[model.namespace]) {
    app.model(model);
    cached[model.namespace] = 1;
  }
}

function RouterConfig({ history, app }) {
  const routes = [
    {
      path: '/',
      name: 'IndexPage',
      getComponent(nextState, cb) {
        require.ensure([], (require) => {
          cb(null, require('./routes/IndexPage'));
        });
      },
    },
    {
      path: 'sign',
      name: 'signPage',
      getComponent(nextState, cb) {
        require.ensure([], (require) => {
          cb(null, require('./routes/session/Login'));
        });
      },
    },
    {
      path: 'admin',
      name: 'adminPage',
      onEnter(nextState, replace) {
        if (localStorage.token === undefined) {
          replace('/sign');
        }
      },
      getComponent(nextState, cb) {
        require.ensure([], (require) => {
          registerModel(app, require('./models/admin'));
          cb(null, require('./routes/Admin'));
        });
      },
      childRoutes: [
        {
          path: 'order',
          name: 'orderPage',
          getComponent(nextState, cb) {
            require.ensure([], (require) => {
              registerModel(app, require('./models/order'));
              cb(null, require('./routes/Order'));
            });
          },
        },
        {
          path: 'user',
          name: 'userPage',
          getComponent(nextState, cb) {
            require.ensure([], (require) => {
              registerModel(app, require('./models/user'));
              cb(null, require('./routes/user'));
            });
          },
        },
        {
          path: 'car',
          name: 'carPage',
          getComponent(nextState, cb) {
            require.ensure([], (require) => {
              registerModel(app, require('./models/car'));
              cb(null, require('./routes/car'));
            });
          },
        },
        {
          path: 'school',
          name: 'schoolPage',
          getComponent(nextState, cb) {
            require.ensure([], (require) => {
              registerModel(app, require('./models/school'));
              cb(null, require('./routes/school'));
            });
          },
        },
        {
          path: 'coupons',
          name: 'couponPage',
          getComponent(nextState, cb) {
            require.ensure([], (require) => {
              registerModel(app, require('./models/coupon'));
              cb(null, require('./routes/coupon'));
            });
          },
        },
        {
          path: 'storage',
          name: 'storagePage',
          getComponent(nextState, cb) {
            require.ensure([], (require) => {
              registerModel(app, require('./models/Storage'));
              cb(null, require('./routes/storage'));
            });
          },
        },
        {
          path: 'store',
          name: 'storePage',
          getComponent(nextState, cb) {
            require.ensure([], (require) => {
              cb(null, require('./routes/store'));
            });
          },
        },
        {
          path: 'battery',
          name: 'batteryPage',
          getComponent(nextState, cb) {
            require.ensure([], (require) => {
              cb(null, require('./routes/battery').default);
            });
          },
        },
        {
          path: 'battery/record',
          getComponent(nextState, cb) {
            require.ensure([], (require) => {
              cb(null, require('./routes/battery').BatteryRecord);
            });
          },
        },
        {
          path: 'battery/report',
          getComponent(nextState, cb) {
            require.ensure([], (require) => {
              cb(null, require('./routes/battery').BatteryReport);
            });
          },
        },
        {
          path: 'report',
          name: 'reportyPage',
          getComponent(nextState, cb) {
            require.ensure([], (require) => {
              cb(null, require('./routes/report'));
            });
          },
        },
        {
          path: 'refund',
          name: 'refundPage',
          getComponent(nextState, cb) {
            require.ensure([], (require) => {
              cb(null, require('./routes/refund'));
            });
          },
        },
        {
          path: 'setting',
          getComponent(nextState, cb) {
            require.ensure([], (require) => {
              cb(null, require('./routes/setting'));
            });
          },
        },
        {
          path: 'NO',
          name: 'NOPage',
          getComponent(nextState, cb) {
            require.ensure([], (require) => {
              cb(null, require('./routes/NO'));
            });
          },
        },
      ],
    },
  ];

  return <Router history={history} routes={routes} />;
}

export default RouterConfig;
