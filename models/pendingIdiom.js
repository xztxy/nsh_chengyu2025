/**
 * 待审核成语模型
 */

const dbUtils = require('../utils/dbUtils');

/**
 * 加载所有待审核成语
 * @returns {Promise<Array>} 待审核成语列表
 */
function loadPendingIdioms() {
  return new Promise((resolve, reject) => {
    const db = dbUtils.getDbConnection();
    db.all('SELECT * FROM pending_idioms', (err, rows) => {
      if (err) {
        reject(err);
      } else {
        resolve(rows);
      }
    });
  });
}

/**
 * 保存待审核成语
 * @param {Object} idiom 待审核成语对象
 * @returns {Promise<void>}
 */
function savePendingIdiom(idiom) {
  return new Promise((resolve, reject) => {
    const db = dbUtils.getDbConnection();
    const sql = `
      INSERT OR REPLACE INTO pending_idioms 
      (word, pinyin_r, weight)
      VALUES (?, ?, ?)
    `;
    const params = [
      idiom.word || '',
      idiom.pinyin_r || '',
      idiom.weight || 0
    ];
    db.run(sql, params, (err) => {
      if (err) {
        reject(err);
      } else {
        resolve();
      }
    });
  });
}

/**
 * 删除待审核成语
 * @param {string} word 成语
 * @returns {Promise<void>}
 */
function deletePendingIdiom(word) {
  return new Promise((resolve, reject) => {
    const db = dbUtils.getDbConnection();
    const sql = 'DELETE FROM pending_idioms WHERE word = ?';
    db.run(sql, [word], (err) => {
      if (err) {
        reject(err);
      } else {
        resolve();
      }
    });
  });
}

/**
 * 检查待审核成语是否存在
 * @param {string} word 成语
 * @returns {Promise<boolean>} 是否存在
 */
function checkPendingIdiomExists(word) {
  return new Promise((resolve, reject) => {
    const db = dbUtils.getDbConnection();
    db.get('SELECT word FROM pending_idioms WHERE word = ?', [word], (err, row) => {
      if (err) {
        reject(err);
      } else {
        resolve(!!row);
      }
    });
  });
}

module.exports = {
  loadPendingIdioms,
  savePendingIdiom,
  deletePendingIdiom,
  checkPendingIdiomExists
};