/**
 * 审核服务
 */

const pendingIdiomModel = require('../models/pendingIdiom');
const idiomService = require('./idiomService');

/**
 * 加载待审核成语
 * @returns {Promise<Array>} 待审核成语列表
 */
async function loadPendingIdioms() {
  try {
    return await pendingIdiomModel.loadPendingIdioms();
  } catch (error) {
    console.error('加载待审核成语时发生错误:', error);
    throw error;
  }
}

/**
 * 审核成语
 * @param {string} word 成语
 * @param {string} action 操作：approve（通过）或 reject（拒绝）
 * @returns {Promise<void>}
 */
async function processIdiom(word, action) {
  try {
    if (action === 'approve') {
      // 获取待审核成语
      const db = require('../utils/dbUtils').getDbConnection();
      const pendingIdiom = await new Promise((resolve, reject) => {
        db.get('SELECT * FROM pending_idioms WHERE word = ?', [word], (err, row) => {
          if (err) {
            reject(err);
          } else {
            resolve(row);
          }
        });
      });
      
      if (pendingIdiom) {
        // 保存到正式库
        await idiomService.saveIdiom(pendingIdiom);
      }
    }
    
    // 从待审核表中删除
    await pendingIdiomModel.deletePendingIdiom(word);
  } catch (error) {
    console.error('审核成语时发生错误:', error);
    throw error;
  }
}

module.exports = {
  loadPendingIdioms,
  processIdiom
};