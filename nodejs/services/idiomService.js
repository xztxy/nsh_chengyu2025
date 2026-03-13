/**
 * 成语服务
 */

const idiomModel = require('../models/idiom');
const pendingIdiomModel = require('../models/pendingIdiom');
const invertedIndexModel = require('../models/invertedIndex');

/**
 * 检查成语是否存在（包括正式成语和待审核成语）
 * @param {string} word 成语
 * @returns {Promise<boolean>} 是否存在
 */
async function checkIdiomExists(word) {
  try {
    // 检查正式成语
    const existsInIdioms = await idiomModel.checkIdiomExists(word);
    if (existsInIdioms) {
      return true;
    }
    
    // 检查待审核成语
    const existsInPending = await pendingIdiomModel.checkPendingIdiomExists(word);
    return existsInPending;
  } catch (error) {
    console.error('检查成语是否存在时发生错误:', error);
    throw error;
  }
}

/**
 * 保存待审核成语
 * @param {Object} idiom 待审核成语对象
 * @returns {Promise<void>}
 */
async function savePendingIdiom(idiom) {
  try {
    await pendingIdiomModel.savePendingIdiom(idiom);
  } catch (error) {
    console.error('保存待审核成语时发生错误:', error);
    throw error;
  }
}

/**
 * 更新成语权重
 * @param {string} word 成语
 * @param {number} weight 权重
 * @returns {Promise<void>}
 */
async function updateIdiomWeight(word, weight) {
  try {
    await idiomModel.updateIdiomWeight(word, weight);
  } catch (error) {
    console.error('更新成语权重时发生错误:', error);
    throw error;
  }
}

/**
 * 保存成语到正式库
 * @param {Object} idiom 成语对象
 * @returns {Promise<void>}
 */
async function saveIdiom(idiom) {
  try {
    await idiomModel.saveIdiom(idiom);
    // 为成语创建倒排索引
    if (idiom.pinyin_r) {
      await invertedIndexModel.createInvertedIndex(idiom.word, idiom.pinyin_r);
    }
  } catch (error) {
    console.error('保存成语到正式库时发生错误:', error);
    throw error;
  }
}

/**
 * 获取成语详情
 * @param {string} word 成语
 * @returns {Promise<Object>} 成语详情
 */
async function getIdiomDetail(word) {
  try {
    return await idiomModel.getIdiomDetail(word);
  } catch (error) {
    console.error('获取成语详情时发生错误:', error);
    throw error;
  }
}

module.exports = {
  checkIdiomExists,
  savePendingIdiom,
  updateIdiomWeight,
  saveIdiom,
  getIdiomDetail
};