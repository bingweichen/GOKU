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
      ],
    },
  ];

  return <Router history={history} routes={routes} />;
}

export default RouterConfig;
