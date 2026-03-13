/**
 * 成语模型
 */

const dbUtils = require('../utils/dbUtils');

/**
 * 加载所有成语
 * @returns {Promise<Array>} 成语列表
 */
function loadIdioms() {
  return new Promise((resolve, reject) => {
    const db = dbUtils.getDbConnection();
    db.all('SELECT * FROM idioms', (err, rows) => {
      if (err) {
        reject(err);
      } else {
        resolve(rows);
      }
    });
  });
}

/**
 * 保存成语
 * @param {Object} idiom 成语对象
 * @returns {Promise<void>}
 */
function saveIdiom(idiom) {
  return new Promise((resolve, reject) => {
    const db = dbUtils.getDbConnection();
    const sql = `
      INSERT OR REPLACE INTO idioms 
      (word, pinyin, pinyin_r, derivation, example, explanation, abbreviation, first, last, weight)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `;
    const params = [
      idiom.word || '',
      idiom.pinyin || '',
      idiom.pinyin_r || '',
      idiom.derivation || '',
      idiom.example || '',
      idiom.explanation || '',
      idiom.abbreviation || '',
      idiom.first || '',
      idiom.last || '',
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
 * 更新成语权重
 * @param {string} word 成语
 * @param {number} weight 权重
 * @returns {Promise<void>}
 */
function updateIdiomWeight(word, weight) {
  return new Promise((resolve, reject) => {
    const db = dbUtils.getDbConnection();
    const sql = 'UPDATE idioms SET weight = ? WHERE word = ?';
    db.run(sql, [weight, word], (err) => {
      if (err) {
        reject(err);
      } else {
        resolve();
      }
    });
  });
}

/**
 * 检查成语是否存在
 * @param {string} word 成语
 * @returns {Promise<boolean>} 是否存在
 */
function checkIdiomExists(word) {
  return new Promise((resolve, reject) => {
    const db = dbUtils.getDbConnection();
    db.get('SELECT word FROM idioms WHERE word = ?', [word], (err, row) => {
      if (err) {
        reject(err);
      } else {
        resolve(!!row);
      }
    });
  });
}

/**
 * 获取成语详情
 * @param {string} word 成语
 * @returns {Promise<Object>} 成语详情
 */
function getIdiomDetail(word) {
  return new Promise((resolve, reject) => {
    const db = dbUtils.getDbConnection();
    db.get('SELECT * FROM idioms WHERE word = ?', [word], (err, row) => {
      if (err) {
        reject(err);
      } else {
        resolve(row);
      }
    });
  });
}

module.exports = {
  loadIdioms,
  saveIdiom,
  updateIdiomWeight,
  checkIdiomExists,
  getIdiomDetail
};