/**
 * API控制器
 */

const idiomService = require('../services/idiomService');

/**
 * 获取成语详情API
 * @param {Object} req 请求对象
 * @param {Object} res 响应对象
 */
async function getIdiomInfo(req, res) {
  try {
    const word = req.params.word;
    const idiomDetail = await idiomService.getIdiomDetail(word);
    
    if (idiomDetail) {
      return res.json({
        success: true,
        data: idiomDetail
      });
    } else {
      return res.status(404).json({
        success: false,
        message: '成语不存在'
      });
    }
  } catch (error) {
    console.error('获取成语详情时发生错误:', error);
    return res.status(500).json({
      success: false,
      message: '系统错误，请稍后重试'
    });
  }
}

module.exports = {
  getIdiomInfo
};