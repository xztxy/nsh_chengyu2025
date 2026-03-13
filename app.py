from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import logging
import hashlib
from config import Config
from db import load_pending_idioms, save_pending_idiom, update_idiom_weight, delete_pending_idiom, check_idiom_exists, save_idiom, get_db_connection, get_idiom_detail
from search import search_idioms, parse_input, get_initials_and_finals

app = Flask(__name__)
app.config.from_object(Config)

# 配置日志
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

# 模板已移至templates目录下的独立文件中

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', idioms=None, error_message=None)

@app.route('/search', methods=['POST'])
def search():
    try:
        include_pinyin = parse_input(request.form.get('include_pinyin', ''))
        exclude_pinyin = parse_input(request.form.get('exclude_pinyin', ''))

        include_initials, include_finals = set(), set()
        exclude_initials, exclude_finals = set(), set()

        for item in include_pinyin:
            initial, final = get_initials_and_finals(item)
            if initial: include_initials.add(initial)
            if final: include_finals.add(final)

        for item in exclude_pinyin:
            initial, final = get_initials_and_finals(item)
            if initial: exclude_initials.add(initial)
            if final: exclude_finals.add(final)

        conflict_initials = include_initials.intersection(exclude_initials)
        conflict_finals = include_finals.intersection(exclude_finals)

        if conflict_initials or conflict_finals:
            conflict_message = "条件冲突: "
            if conflict_initials:
                conflict_message += "声母 - " + ", ".join(conflict_initials)
            if conflict_finals:
                if conflict_initials:
                    conflict_message += "; "
                conflict_message += "韵母 - " + ", ".join(conflict_finals)
            return render_template('index.html', idioms=None, error_message=conflict_message)

        position_include_conditions = []
        position_exclude_conditions = []

        for i in range(4):
            pi_conditions = parse_input(request.form.get(f'position{i}_include', ''))
            pe_conditions = parse_input(request.form.get(f'position{i}_exclude', ''))

            pi_initials, pi_finals = set(), set()
            pe_initials, pe_finals = set(), set()

            for item in pi_conditions:
                initial, final = get_initials_and_finals(item)
                if initial: pi_initials.add(initial)
                if final: pi_finals.add(final)

            for item in pe_conditions:
                initial, final = get_initials_and_finals(item)
                if initial: pe_initials.add(initial)
                if final: pe_finals.add(final)

            position_include_conditions.append((pi_initials, pi_finals))
            position_exclude_conditions.append((pe_initials, pe_finals))

        matched_idioms = search_idioms(
            include_initials, include_finals,
            exclude_initials, exclude_finals,
            position_include_conditions,
            position_exclude_conditions
        )

        # 更新权重但限制频率
        if len(matched_idioms) < 5 and len(matched_idioms) > 0:
            for idiom in matched_idioms:
                # 从数据库获取当前成语
                conn = get_db_connection()
                c = conn.cursor()
                c.execute('SELECT weight FROM idioms WHERE word = ?', (idiom['word'],))
                result = c.fetchone()
                if result:
                    new_weight = result['weight'] + 1
                    update_idiom_weight(idiom['word'], new_weight)
                conn.close()

        if not matched_idioms:
            return render_template('index.html', idioms=[], error_message=None)
        
        return render_template('index.html', idioms=matched_idioms, error_message=None)
    except Exception as e:
        logger.error(f"搜索过程中发生错误: {str(e)}")
        return render_template('index.html', idioms=None, error_message="系统错误，请稍后重试")

@app.route('/add_idiom', methods=['POST'])
def add_idiom():
    try:
        new_idiom = request.form.get('new_idiom').strip()
        new_pinyin = request.form.get('new_pinyin').strip()

        # 输入验证
        if not new_idiom or not new_pinyin:
            return render_template('index.html', idioms=None, error_message="Error: 成语和拼音不能为空")

        if len(new_idiom) != 4:
            return render_template('index.html', idioms=None, error_message="Error: 成语必须为四个字的长度")

        # 验证拼音格式（简单验证）
        import re
        if not re.match(r'^[a-zA-ZüÜ\s]+$', new_pinyin):
            return render_template('index.html', idioms=None, error_message="Error: 拼音格式不正确")

        # 检查成语是否已存在
        if check_idiom_exists(new_idiom):
            return render_template('index.html', idioms=None, error_message="Error: 成语已存在或在待审核列表中")

        new_entry = {
            'word': new_idiom,
            'pinyin_r': new_pinyin,
            'weight': 0
        }
        save_pending_idiom(new_entry)

        logger.info(f"新成语已添加至待审核列表: {new_idiom}")
        return render_template('index.html', idioms=None, error_message="成语已成功添加至待审核列表")
    except Exception as e:
        logger.error(f"添加成语过程中发生错误: {str(e)}")
        return render_template('index.html', idioms=None, error_message="系统错误，请稍后重试")

@app.route('/review', methods=['GET', 'POST'])
def review():
    if request.method == 'POST':
        password = request.form.get('password', '').strip()
        # 使用hash比较提高安全性
        if hashlib.sha256(password.encode()).hexdigest() == hashlib.sha256(Config.SECRET_PASSWORD.encode()).hexdigest():
            session['authenticated'] = True
            logger.info("管理员已登录审核界面")
            return redirect(url_for('review'))

    if not session.get('authenticated', False):
        return render_template('review_login.html')

    pending_idioms = load_pending_idioms()
    return render_template('review.html', idioms=pending_idioms)

@app.route('/process_idiom', methods=['POST'])
def process_idiom():
    if not session.get('authenticated', False):
        logger.warning("未授权用户尝试访问成语处理功能")
        return redirect(url_for('review'))

    action = request.form.get('action')
    word = request.form.get('word')

    # 输入验证
    if action not in ['approve', 'reject'] or not word:
        logger.warning(f"无效的处理请求: action={action}, word={word}")
        return redirect(url_for('review'))

    # 从数据库获取待审核成语
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM pending_idioms WHERE word = ?', (word,))
    pending_idiom = c.fetchone()
    conn.close()

    if not pending_idiom:
        logger.warning(f"尝试处理不存在的待审核成语: {word}")
        return redirect(url_for('review'))

    if action == 'approve':
        # 将待审核成语添加到正式成语表
        idiom_dict = dict(pending_idiom)
        save_idiom(idiom_dict)
        # 从待审核表中删除
        delete_pending_idiom(word)
        logger.info(f"成语 '{word}' 已通过审核并添加到词库")
    elif action == 'reject':
        # 从待审核表中删除
        delete_pending_idiom(word)
        logger.info(f"成语 '{word}' 已被拒绝")

    return redirect(url_for('review'))

@app.route('/api/idiom/<word>', methods=['GET'])
def get_idiom_info(word):
    """获取成语详情API"""
    try:
        idiom_detail = get_idiom_detail(word)
        if idiom_detail:
            return jsonify({
                'success': True,
                'data': idiom_detail
            })
        else:
            return jsonify({
                'success': False,
                'message': '成语不存在'
            }), 404
    except Exception as e:
        logger.error(f"获取成语详情时发生错误: {str(e)}")
        return jsonify({
            'success': False,
            'message': '系统错误，请稍后重试'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)