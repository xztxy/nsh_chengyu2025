/**
 * 添加成语控制器
 */

const idiomService = require('../services/idiomService');
const pinyinUtils = require('../utils/pinyinUtils');

/**
 * 处理添加成语请求
 * @param {Object} req 请求对象
 * @param {Object} res 响应对象
 */
async function addIdiom(req, res) {
  try {
    const newIdiom = req.body.new_idiom?.trim();
    const newPinyin = req.body.new_pinyin?.trim();

    // 输入验证
    if (!newIdiom || !newPinyin) {
      return res.render('index', { idioms: null, error_message: "Error: 成语和拼音不能为空" });
    }

    if (newIdiom.length !== 4) {
      return res.render('index', { idioms: null, error_message: "Error: 成语必须为四个字的长度" });
    }

    // 验证拼音格式（简单验证）
    if (!pinyinUtils.validatePinyinFormat(newPinyin)) {
      return res.render('index', { idioms: null, error_message: "Error: 拼音格式不正确" });
    }

    // 检查成语是否已存在
    const exists = await idiomService.checkIdiomExists(newIdiom);
    if (exists) {
      return res.render('index', { idioms: null, error_message: "Error: 成语已存在或在待审核列表中" });
    }

    // 保存待审核成语
    const newEntry = {
      word: newIdiom,
      pinyin_r: newPinyin,
      weight: 0
    };
    await idiomService.savePendingIdiom(newEntry);

    console.log(`新成语已添加至待审核列表: ${newIdiom}`);
    return res.render('index', { idioms: null, error_message: "成语已成功添加至待审核列表" });
  } catch (error) {
    console.error('添加成语过程中发生错误:', error);
    return res.render('index', { idioms: null, error_message: "系统错误，请稍后重试" });
  }
}

module.exports = {
  addIdiom
};