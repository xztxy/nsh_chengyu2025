/**
 * 搜索控制器
 */

const searchService = require('../services/searchService');
const pinyinUtils = require('../utils/pinyinUtils');

/**
 * 处理搜索请求
 * @param {Object} req 请求对象
 * @param {Object} res 响应对象
 */
async function search(req, res) {
  try {
    const includePinyin = pinyinUtils.parseInput(req.body.include_pinyin || '');
    const excludePinyin = pinyinUtils.parseInput(req.body.exclude_pinyin || '');

    const includeInitials = new Set();
    const includeFinals = new Set();
    const excludeInitials = new Set();
    const excludeFinals = new Set();

    // 处理包含的拼音条件
    for (const item of includePinyin) {
      const [initial, final] = pinyinUtils.getInitialsAndFinals(item);
      if (initial) includeInitials.add(initial);
      if (final) includeFinals.add(final);
    }

    // 处理排除的拼音条件
    for (const item of excludePinyin) {
      const [initial, final] = pinyinUtils.getInitialsAndFinals(item);
      if (initial) excludeInitials.add(initial);
      if (final) excludeFinals.add(final);
    }

    // 检查条件冲突
    const conflictInitials = new Set([...includeInitials].filter(initial => excludeInitials.has(initial)));
    const conflictFinals = new Set([...includeFinals].filter(final => excludeFinals.has(final)));

    if (conflictInitials.size > 0 || conflictFinals.size > 0) {
      let conflictMessage = "条件冲突: ";
      if (conflictInitials.size > 0) {
        conflictMessage += "声母 - " + Array.from(conflictInitials).join(", ");
      }
      if (conflictFinals.size > 0) {
        if (conflictInitials.size > 0) {
          conflictMessage += "; ";
        }
        conflictMessage += "韵母 - " + Array.from(conflictFinals).join(", ");
      }
      return res.render('index', { idioms: null, error_message: conflictMessage });
    }

    // 处理位置条件
    const positionIncludeConditions = [];
    const positionExcludeConditions = [];

    for (let i = 0; i < 4; i++) {
      const piConditions = pinyinUtils.parseInput(req.body[`position${i}_include`] || '');
      const peConditions = pinyinUtils.parseInput(req.body[`position${i}_exclude`] || '');

      const piInitials = new Set();
      const piFinals = new Set();
      const peInitials = new Set();
      const peFinals = new Set();

      for (const item of piConditions) {
        const [initial, final] = pinyinUtils.getInitialsAndFinals(item);
        if (initial) piInitials.add(initial);
        if (final) piFinals.add(final);
      }

      for (const item of peConditions) {
        const [initial, final] = pinyinUtils.getInitialsAndFinals(item);
        if (initial) peInitials.add(initial);
        if (final) peFinals.add(final);
      }

      positionIncludeConditions.push([Array.from(piInitials), Array.from(piFinals)]);
      positionExcludeConditions.push([Array.from(peInitials), Array.from(peFinals)]);
    }

    // 搜索成语
    const matchedIdioms = await searchService.searchIdioms(
      Array.from(includeInitials),
      Array.from(includeFinals),
      Array.from(excludeInitials),
      Array.from(excludeFinals),
      positionIncludeConditions,
      positionExcludeConditions
    );

    // 更新权重但限制频率
    if (matchedIdioms.length < 5 && matchedIdioms.length > 0) {
      for (const idiom of matchedIdioms) {
        // 从数据库获取当前成语
        const db = require('../utils/dbUtils').getDbConnection();
        const currentWeight = await new Promise((resolve, reject) => {
          db.get('SELECT weight FROM idioms WHERE word = ?', [idiom.word], (err, row) => {
            if (err) {
              reject(err);
            } else {
              resolve(row ? row.weight : 0);
            }
          });
        });
        
        const newWeight = currentWeight + 1;
        await require('../services/idiomService').updateIdiomWeight(idiom.word, newWeight);
      }
    }

    return res.render('index', { idioms: matchedIdioms, error_message: null });
  } catch (error) {
    console.error('搜索过程中发生错误:', error);
    return res.render('index', { idioms: null, error_message: "系统错误，请稍后重试" });
  }
}

module.exports = {
  search
};