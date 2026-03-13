/**
 * 搜索服务
 */

const idiomModel = require('../models/idiom');
const invertedIndexModel = require('../models/invertedIndex');
const pinyinUtils = require('../utils/pinyinUtils');

/**
 * 搜索成语
 * @param {Array} includeInitials 包含的声母
 * @param {Array} includeFinals 包含的韵母
 * @param {Array} excludeInitials 排除的声母
 * @param {Array} excludeFinals 排除的韵母
 * @param {Array} positionIncludeConditions 位置包含条件
 * @param {Array} positionExcludeConditions 位置排除条件
 * @returns {Promise<Array>} 符合条件的成语列表
 */
async function searchIdioms(includeInitials, includeFinals, excludeInitials, excludeFinals, positionIncludeConditions, positionExcludeConditions) {
  try {
    // 使用倒排索引快速过滤成语
    const includedWords = await invertedIndexModel.searchByPinyinElements(
      includeInitials, 
      includeFinals, 
      excludeInitials, 
      excludeFinals
    );
    
    // 获取候选成语的详细信息
    let candidateIdioms = [];
    if (includedWords.size > 0) {
      const db = require('../utils/dbUtils').getDbConnection();
      const placeholders = Array.from(includedWords).map(() => '?').join(',');
      const query = `SELECT word, pinyin_r, weight FROM idioms WHERE word IN (${placeholders}) ORDER BY weight DESC`;
      
      candidateIdioms = await new Promise((resolve, reject) => {
        db.all(query, Array.from(includedWords), (err, rows) => {
          if (err) {
            reject(err);
          } else {
            resolve(rows);
          }
        });
      });
    }
    
    // 进一步过滤位置条件
    const resultIdioms = [];
    for (const idiom of candidateIdioms) {
      const { word, pinyin_r, weight } = idiom;
      
      if (word.length !== 4 || pinyin_r.split(' ').length !== 4) {
        continue;
      }

      const pinyinList = pinyin_r.split(' ');
      const initialMatches = pinyinList.map(pinyin => pinyinUtils.getInitialsAndFinals(pinyin)[0]);
      const finalMatches = pinyinList.map(pinyin => pinyinUtils.getInitialsAndFinals(pinyin)[1]);

      // 检查位置条件
      let satisfiesPositionConditions = true;
      for (let i = 0; i < 4; i++) {
        const [includeInitials, includeFinals] = positionIncludeConditions[i];
        const [excludeInitials, excludeFinals] = positionExcludeConditions[i];
        
        // 检查包含条件
        const includesInitials = includeInitials.length === 0 || includeInitials.includes(initialMatches[i]);
        const includesFinals = includeFinals.length === 0 || includeFinals.includes(finalMatches[i]);
        
        // 检查排除条件
        const excludesInitials = excludeInitials.length === 0 || !excludeInitials.includes(initialMatches[i]);
        const excludesFinals = excludeFinals.length === 0 || !excludeFinals.includes(finalMatches[i]);
        
        if (!includesInitials || !includesFinals || !excludesInitials || !excludesFinals) {
          satisfiesPositionConditions = false;
          break;
        }
      }

      if (satisfiesPositionConditions) {
        resultIdioms.push({ word, pinyin: pinyin_r, weight });
      }
    }

    // 按权重排序
    resultIdioms.sort((a, b) => b.weight - a.weight);
    return resultIdioms;
  } catch (error) {
    console.error('搜索成语时发生错误:', error);
    throw error;
  }
}

module.exports = {
  searchIdioms
};