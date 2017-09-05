const pxtorem = require('postcss-pxtorem');
const path = require('path');
const svgSpriteDirs = [
  require.resolve('antd-mobile').replace(/warn\.js$/, ''), // antd-mobile 内置svg
  path.resolve(__dirname, 'src/assets/image'),  // 业务代码本地私有 svg 存放目录
];

export default {
  "entry": "src/index.js",
  "env": {
    "development": {
      "extraBabelPlugins": [
        "dva-hmr",
        "transform-runtime",
        ["import", { "libraryName": "antd-mobile", "libraryDirectory": "lib", "style": "css" }]
      ]
    },
    "production": {
      "extraBabelPlugins": [
        "dva-hmr",
        "transform-runtime",
        ["import", { "libraryName": "antd-mobile", "libraryDirectory": "lib", "style": "css" }]
      ]
    }
  },
  "extraPostCSSPlugins": [
    pxtorem({
      rootValue: 100,
      propWhiteList: [],
    }),
  ],
  "autoprefixer": {
    "browsers": [
      "iOS >= 8", "Android >= 4"
    ]
  },
  "svgSpriteLoaderDirs": svgSpriteDirs,
  "proxy": {
    "/api": {
      // "target": "http://localhost:3333/",
      // "target": "http://192.168.31.70:5000/",
      // "target": "http://192.168.31.228:5000",
      "target": "http://localhost:5000",
      "changeOrigin": true,
      "pathRewrite": { "^/api": "" }
    }
  }
}
