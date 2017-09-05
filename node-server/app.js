const express = require('express')
const request = require('request');
const crypto = require('crypto');
const app = express()


app.use('/admin', express.static('../goku-admin/index.html'));
app.use('/dist', express.static('../goku-admin/dist'));

app.use('/api', function (req, res) {
  var url = 'http://localhost:5000' + req.url;
  console.log(url)
  req.pipe(request(url)).pipe(res);
});

app.use('/wx', function (req, res) {
  const token = 'schooltrip';
  console.log(req)
  const params = req.query;
  console.log(params);
  const signature = params.signature;
  const timestamp = params.timestamp;
  const nonce = params.nonce;
  let tmpArr = [token, timestamp, nonce];
  tmpArr.sort();
  let sha1 = crypto.createHash('sha1');
  let msg = tmpArr[0] + tmpArr[1] + tmpArr[2];
  sha1.update(msg);
  msg = sha1.digest('hex');
  if (msg == signature) {
    console.log('验证成功');
    res.send(query.echostr);
  } else {
    console.log('验证失败');
    res.send('微信登录验证失败，请重试！');
  }
})

app.listen(8889, function () {
  console.log('Example app listening on port 3000!')
})