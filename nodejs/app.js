/**
 * 应用入口
 */

const express = require('express');
const session = require('express-session');
const bodyParser = require('body-parser');
const path = require('path');
const config = require('./config/config');

// 初始化Express应用
const app = express();

// 配置模板引擎
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'templates'));

// 配置中间件
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(session({
  secret: config.SECRET_KEY,
  resave: false,
  saveUninitialized: true,
  cookie: { secure: false }
}));

// 挂载路由
const routes = require('./routes');
app.use('/', routes);

// 初始化数据库
const dbUtils = require('./utils/dbUtils');
dbUtils.getDbConnection();

// 启动服务器
const port = config.PORT;
app.listen(port, () => {
  console.log(`服务器运行在 http://localhost:${port}`);
});

module.exports = app;