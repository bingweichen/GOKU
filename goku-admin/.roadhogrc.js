export default {
  "entry": "src/index.js",
  "env": {
    "development": {
      "extraBabelPlugins": [
        "dva-hmr",
        "transform-runtime",
        ["import", { "libraryName": "antd", "style": true }]
      ]
    },
    "production": {
      "extraBabelPlugins": [
        "transform-runtime",
        "dva-hmr",
        ["import", { "libraryName": "antd", "style": true }]
      ],
      "publicPath": "./dist/",
    }
  },
  "proxy": {
    "/api": {
      // "target": "http://jsonplaceholder.typicode.com/",
      "target": "http://localhost:5000",
      "changeOrigin": true,
      "pathRewrite": { "^/api": "" }
    }
  }
}
