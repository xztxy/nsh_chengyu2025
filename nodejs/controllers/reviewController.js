/**
 * 审核控制器
 */

const reviewService = require('../services/reviewService');
const config = require('../config/config');

/**
 * 处理审核登录请求
 * @param {Object} req 请求对象
 * @param {Object} res 响应对象
 */
async function review(req, res) {
  if (req.method === 'POST') {
    const password = req.body.password?.trim();
    // 使用简单的密码比较（实际应用中应该使用加密）
    if (password === config.SECRET_PASSWORD) {
      req.session.authenticated = true;
      console.log('管理员已登录审核界面');
      return res.redirect('/review');
    } else {
      return res.render('review_login', { error: '密码错误' });
    }
  }

  if (!req.session.authenticated) {
    return res.render('review_login', { error: null });
  }

  try {
    const pendingIdioms = await reviewService.loadPendingIdioms();
    return res.render('review', { idioms: pendingIdioms });
  } catch (error) {
    console.error('加载待审核成语时发生错误:', error);
    return res.render('review', { idioms: [] });
  }
}

/**
 * 处理审核操作请求
 * @param {Object} req 请求对象
 * @param {Object} res 响应对象
 */
async function processIdiom(req, res) {
  if (!req.session.authenticated) {
    console.warn('未授权用户尝试访问成语处理功能');
    return res.redirect('/review');
  }

  const action = req.body.action;
  const word = req.body.word;

  // 输入验证
  if (!action || !word || !['approve', 'reject'].includes(action)) {
    console.warn(`无效的处理请求: action=${action}, word=${word}`);
    return res.redirect('/review');
  }

  try {
    await reviewService.processIdiom(word, action);
    console.log(`成语 '${word}' 已被${action === 'approve' ? '通过审核并添加到词库' : '拒绝'}`);
    return res.redirect('/review');
  } catch (error) {
    console.error('审核成语时发生错误:', error);
    return res.redirect('/review');
  }
}

module.exports = {
  review,
  processIdiom
};