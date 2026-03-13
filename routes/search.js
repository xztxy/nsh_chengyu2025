/**
 * 搜索路由
 */

const express = require('express');
const router = express.Router();
const searchController = require('../controllers/searchController');

// 搜索路由
router.post('/', searchController.search);

module.exports = router;