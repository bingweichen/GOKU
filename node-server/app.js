const express = require('express')
const request = require('request');
const app = express()


app.use('/admin', express.static('../goku-admin/index.html'));
app.use('/dist', express.static('../goku-admin/dist'));

app.use('/api', function (req, res) {
  var url = 'http://localhost:5000' + req.url;
  console.log(url)
  req.pipe(request(url)).pipe(res);
});

app.listen(80, function () {
  console.log('Example app listening on port 3000!')
})