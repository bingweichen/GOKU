import dva from 'dva';
import './index.less';

// 1. Initialize
const app = dva();

// 2. Plugins
// app.use({});

// 3. Model
// app.model(require('./models/example'));
app.model(require('./models/IndexPage'));

app.model(require('./models/person'));

app.model(require('./models/order'));

app.model(require('./models/shop'));

app.model(require('./models/battery'));

// 4. Router
app.router(require('./router'));

// 5. Start
app.start('#root');
