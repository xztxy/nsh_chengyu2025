/**
 * 审核路由
 */

const express = require('express');
const router = express.Router();
const reviewController = require('../controllers/reviewController');

// 审核登录和加载待审核成语路由
router.get('/', reviewController.review);
router.post('/', reviewController.review);

// 处理审核操作路由
router.post('/process_idiom', reviewController.processIdiom);

module.exports = router;