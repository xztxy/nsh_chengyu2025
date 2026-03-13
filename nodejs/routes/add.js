/**
 * 添加成语路由
 */

const express = require('express');
const router = express.Router();
const addController = require('../controllers/addController');

// 添加成语路由
router.post('/', addController.addIdiom);

module.exports = router;