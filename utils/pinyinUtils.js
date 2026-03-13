/**
 * 拼音处理工具
 */

// 预编译声母和韵母列表
const INITIALS_LIST = ["zh", "ch", "sh", "b", "p", "m", "f", "d", "t", "n", "l", "g", "k", "h", "j", "q", "x", "r", "z", "c", "s", "y", "w"];
const FINALS_LIST = ["a", "o", "e", "i", "u", "ü", "ai", "ei", "ui", "ao", "ou", "iu", "ie", "ia", "v", "üe", "er", "an", "en", "in", "un", "ün", "ang", "eng", "ing", "ong", "iao", "ian", "ia", "iang", "iong", "ua", "uo", "uai", "uan", "uang", "ueng", "ue"];

// 创建声母映射以提高查找性能
const INITIALS_MAP = {};
INITIALS_LIST.forEach(initial => {
  INITIALS_MAP[initial] = initial;
});

/**
 * 验证拼音格式是否正确
 * @param {string} pinyin 待验证的拼音字符串
 * @returns {boolean} 拼音格式是否正确
 */
function validatePinyinFormat(pinyin) {
  if (!pinyin) {
    return false;
  }
  // 允许字母、üÜ和空格
  return /^[a-zA-Z\u00fc\u00dc\s]+$/.test(pinyin);
}

/**
 * 分离声母和韵母
 * @param {string} pinyin 拼音字符串
 * @returns {Array} [声母, 韵母]
 */
function getInitialsAndFinals(pinyin) {
  // 查找声母
  let initial = '';
  // 先检查双字符声母
  if (pinyin.length >= 2) {
    const twoChar = pinyin.substring(0, 2);
    if (INITIALS_MAP[twoChar]) {
      initial = twoChar;
    }
  }
  
  // 如果没有找到双字符声母，检查单字符声母
  if (!initial && pinyin.length >= 1) {
    const oneChar = pinyin.substring(0, 1);
    if (INITIALS_MAP[oneChar]) {
      initial = oneChar;
    }
  }
  
  // 提取韵母
  const final = pinyin.substring(initial.length);
  return [initial, final];
}

/**
 * 解析用户输入的拼音条件
 * @param {string} inputStr 用户输入的拼音条件
 * @returns {Array} 解析后的拼音条件数组
 */
function parseInput(inputStr) {
  return inputStr.split(/[^a-zA-ZüÜ]+/).filter(item => item);
}

module.exports = {
  validatePinyinFormat,
  getInitialsAndFinals,
  parseInput
};