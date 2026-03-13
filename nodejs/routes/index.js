/**
 * 路由入口
 */

const express = require('express');
const router = express.Router();

// 导入路由
const searchRouter = require('./search');
const addRouter = require('./add');
const reviewRouter = require('./review');
const apiRouter = require('./api');

// 首页路由
router.get('/', (req, res) => {
  res.render('index', { idioms: null, error_message: null });
});

// 挂载其他路由
router.use('/search', searchRouter);
router.use('/add_idiom', addRouter);
router.use('/review', reviewRouter);
router.use('/api', apiRouter);

module.exports = router;