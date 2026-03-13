/**
 * 倒排索引模型
 */

const dbUtils = require('../utils/dbUtils');
const pinyinUtils = require('../utils/pinyinUtils');

/**
 * 为成语创建倒排索引
 * @param {string} word 成语
 * @param {string} pinyin 拼音
 * @returns {Promise<void>}
 */
function createInvertedIndex(word, pinyin) {
  return new Promise((resolve, reject) => {
    const db = dbUtils.getDbConnection();
    const pinyinList = pinyin.split(' ');
    
    // 开始事务
    db.serialize(() => {
      // 先删除该成语的旧索引
      db.run('DELETE FROM inverted_index WHERE idiom_word = ?', [word], (err) => {
        if (err) {
          reject(err);
          return;
        }
        
        // 为每个拼音创建索引
        pinyinList.forEach((pinyin, index) => {
          const [initial, final] = pinyinUtils.getInitialsAndFinals(pinyin);
          
          // 为声母创建索引
          if (initial) {
            db.run(
              'INSERT INTO inverted_index (idiom_word, pinyin_element, element_type, position) VALUES (?, ?, ?, ?)',
              [word, initial, 'initial', index]
            );
          }
          
          // 为韵母创建索引
          if (final) {
            db.run(
              'INSERT INTO inverted_index (idiom_word, pinyin_element, element_type, position) VALUES (?, ?, ?, ?)',
              [word, final, 'final', index]
            );
          }
        });
        
        resolve();
      });
    });
  });
}

/**
 * 根据拼音元素搜索成语
 * @param {Array} includeInitials 包含的声母
 * @param {Array} includeFinals 包含的韵母
 * @param {Array} excludeInitials 排除的声母
 * @param {Array} excludeFinals 排除的韵母
 * @returns {Promise<Set>} 符合条件的成语集合
 */
function searchByPinyinElements(includeInitials, includeFinals, excludeInitials, excludeFinals) {
  return new Promise((resolve, reject) => {
    const db = dbUtils.getDbConnection();
    let includedWords = new Set();
    
    // 构建包含条件的查询
    if (includeInitials.length > 0 || includeFinals.length > 0) {
      const conditions = [];
      const params = [];
      
      // 添加声母条件
      includeInitials.forEach(initial => {
        conditions.push('(pinyin_element = ? AND element_type = "initial")');
        params.push(initial);
      });
      
      // 添加韵母条件
      includeFinals.forEach(final => {
        conditions.push('(pinyin_element = ? AND element_type = "final")');
        params.push(final);
      });
      
      if (conditions.length > 0) {
        const query = `
          SELECT idiom_word, COUNT(DISTINCT pinyin_element) as match_count
          FROM inverted_index
          WHERE ${conditions.join(' OR ')}
          GROUP BY idiom_word
          HAVING match_count = ?
        `;
        params.push(includeInitials.length + includeFinals.length);
        
        db.all(query, params, (err, rows) => {
          if (err) {
            reject(err);
            return;
          }
          
          rows.forEach(row => {
            includedWords.add(row.idiom_word);
          });
          
          // 构建排除条件的查询
          if (excludeInitials.length > 0 || excludeFinals.length > 0) {
            const excludeConditions = [];
            const excludeParams = [];
            
            // 添加排除的声母
            excludeInitials.forEach(initial => {
              excludeConditions.push('(pinyin_element = ? AND element_type = "initial")');
              excludeParams.push(initial);
            });
            
            // 添加排除的韵母
            excludeFinals.forEach(final => {
              excludeConditions.push('(pinyin_element = ? AND element_type = "final")');
              excludeParams.push(final);
            });
            
            if (excludeConditions.length > 0) {
              const excludeQuery = `
                SELECT DISTINCT idiom_word
                FROM inverted_index
                WHERE ${excludeConditions.join(' OR ')}
              `;
              
              db.all(excludeQuery, excludeParams, (err, excludeRows) => {
                if (err) {
                  reject(err);
                  return;
                }
                
                // 从包含列表中移除排除的成语
                excludeRows.forEach(row => {
                  includedWords.delete(row.idiom_word);
                });
                
                resolve(includedWords);
              });
            } else {
              resolve(includedWords);
            }
          } else {
            resolve(includedWords);
          }
        });
      } else {
        // 如果没有包含条件，获取所有成语
        db.all('SELECT word FROM idioms', (err, rows) => {
          if (err) {
            reject(err);
            return;
          }
          
          rows.forEach(row => {
            includedWords.add(row.word);
          });
          
          resolve(includedWords);
        });
      }
    } else {
      // 如果没有包含条件，获取所有成语
      db.all('SELECT word FROM idioms', (err, rows) => {
        if (err) {
          reject(err);
          return;
        }
        
        rows.forEach(row => {
          includedWords.add(row.word);
        });
        
        resolve(includedWords);
      });
    }
  });
}

module.exports = {
  createInvertedIndex,
  searchByPinyinElements
};