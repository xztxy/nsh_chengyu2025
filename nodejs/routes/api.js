/**
 * API路由
 */

const express = require('express');
const router = express.Router();
const apiController = require('../controllers/apiController');

// 获取成语详情API路由
router.get('/idiom/:word', apiController.getIdiomInfo);

module.exports = router;