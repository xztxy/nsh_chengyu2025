from flask import Flask, request, render_template, redirect, url_for, session
import json
import re
import os
from flask_caching import Cache
import logging
import hashlib
import secrets

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(16))  # 用于会话管理的密钥
# 在生产环境中，建议使用固定的密钥并存储在环境变量中，以避免每次重启应用时生成新的密钥导致会话失效
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)  # 使用简单内存缓存

IDIOM_FILE_PATH = os.getenv('IDIOM_FILE_PATH', 'data/idiom.json')
PENDING_IDIOM_FILE_PATH = os.getenv('PENDING_IDIOM_FILE_PATH', 'data/pending_idiom.json')
SECRET_PASSWORD = os.getenv('SECRET_PASSWORD', 'lsz20100')

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_idioms(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            idioms = json.load(file)
    else:
        idioms = []
    return idioms

def save_idioms(idioms, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(idioms, file, ensure_ascii=False, indent=4)

# 预编译声母和韵母列表以提高性能
INITIALS_LIST = ["zh", "ch", "sh", "b", "p", "m", "f", "d", "t", "n", "l", "g", "k", "h", "j", "q", "x", "r", "z", "c", "s", "y", "w"]
FINALS_LIST = ["a", "o", "e", "i", "u", "ü", "ai", "ei", "ui", "ao", "ou", "iu", "ie", "ia", "v", "üe", "er", "an", "en", "in", "un", "ün", "ang", "eng",
               "ing", "ong", "iao", "ian", "ia", "iang", "iong", "ua", "uo", "uai", "uan", "uang", "ueng", "ue"]

# 创建声母映射以提高查找性能
INITIALS_MAP = {}
for initial in INITIALS_LIST:
    INITIALS_MAP[initial] = initial


def validate_pinyin_format(pinyin):
    """验证拼音格式是否正确
    
    Args:
        pinyin (str): 待验证的拼音字符串
        
    Returns:
        bool: 拼音格式是否正确
    """
    if not pinyin:
        return False
    # 允许字母、üÜ和空格
    return bool(re.match(r'^[a-zA-Z\u00fc\u00dc\s]+$', pinyin))

def get_initials_and_finals(pinyin):
    """优化的声母韵母分离函数
    
    Args:
        pinyin (str): 拼音字符串
        
    Returns:
        tuple: (声母, 韵母)
    """
    # 查找声母
    initial = ''
    # 先检查双字符声母
    if len(pinyin) >= 2:
        two_char = pinyin[:2]
        if two_char in INITIALS_MAP:
            initial = two_char
    
    # 如果没有找到双字符声母，检查单字符声母
    if not initial and len(pinyin) >= 1:
        one_char = pinyin[:1]
        if one_char in INITIALS_MAP:
            initial = one_char
    
    # 提取韵母
    final = pinyin[len(initial):]
    return initial, final

def parse_input(input_str):
    return re.split(r'[^a-zA-ZüÜ]+', input_str)

@cache.memoize(timeout=60)  # 缓存搜索结果60秒
def search_idioms(idioms, include_initials, include_finals, exclude_initials, exclude_finals,
                  position_include_conditions, position_exclude_conditions):
    """搜索符合条件的成语
    
    Args:
        idioms (list): 成语列表
        include_initials (set): 包含的声母集合
        include_finals (set): 包含的韵母集合
        exclude_initials (set): 排除的声母集合
        exclude_finals (set): 排除的韵母集合
        position_include_conditions (list): 位置包含条件列表
        position_exclude_conditions (list): 位置排除条件列表
        
    Returns:
        list: 符合条件的成语列表
    """
    result_idioms = []
    for idiom in idioms:
        if len(idiom['word']) != 4 or len(idiom['pinyin_r'].split()) != 4:
            continue

        pinyin_list = idiom['pinyin_r'].split()
        initial_matches = [get_initials_and_finals(pinyin)[0] for pinyin in pinyin_list]
        final_matches = [get_initials_and_finals(pinyin)[1] for pinyin in pinyin_list]

        def matches_conditions(initials, finals, include_cond, exclude_cond):
            include_initials, include_finals = include_cond
            exclude_initials, exclude_finals = exclude_cond

            return all(x in initials for x in include_initials) and \
                   all(x in finals for x in include_finals) and \
                   not any(x in initials for x in exclude_initials) and \
                   not any(x in finals for x in exclude_finals)

        if not matches_conditions(initial_matches, final_matches, (include_initials, include_finals), (exclude_initials, exclude_finals)):
            continue

        satisfies_position_conditions = True
        for i in range(4):
            if not matches_conditions([initial_matches[i]], [final_matches[i]], position_include_conditions[i], position_exclude_conditions[i]):
                satisfies_position_conditions = False
                break

        if satisfies_position_conditions:
            result_idioms.append({'word': idiom['word'], 'pinyin': idiom['pinyin_r'], 'weight': idiom['weight']})

    result_idioms.sort(key=lambda x: x['weight'], reverse=True)
    return result_idioms

# 模板已移至templates目录下的独立文件中

@app.route('/', methods=['GET'])
@cache.cached(timeout=300)  # 缓存主页五分钟
def index():
    return render_template('index.html', idioms=None, error_message=None)

@app.route('/search', methods=['POST'])
def search():
    try:
        idioms = load_idioms(IDIOM_FILE_PATH)

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
            idioms, include_initials, include_finals,
            exclude_initials, exclude_finals,
            position_include_conditions,
            position_exclude_conditions
        )

        # 更新权重但限制频率
        if len(matched_idioms) < 5 and len(matched_idioms) > 0:
            for idiom in matched_idioms:
                for orig_idiom in idioms:
                    if orig_idiom['word'] == idiom['word']:
                        orig_idiom['weight'] += 1
            save_idioms(idioms, IDIOM_FILE_PATH)

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
        if not re.match(r'^[a-zA-ZüÜ\s]+$', new_pinyin):
            return render_template('index.html', idioms=None, error_message="Error: 拼音格式不正确")

        current_idioms = load_idioms(IDIOM_FILE_PATH)
        pending_idioms = load_idioms(PENDING_IDIOM_FILE_PATH)

        for idiom in current_idioms + pending_idioms:
            if idiom['word'] == new_idiom:
                return render_template('index.html', idioms=None, error_message="Error: 成语已存在或在待审核列表中")

        new_entry = {
            'word': new_idiom,
            'pinyin_r': new_pinyin,
            'weight': 0
        }
        pending_idioms.append(new_entry)
        save_idioms(pending_idioms, PENDING_IDIOM_FILE_PATH)

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
        if hashlib.sha256(password.encode()).hexdigest() == hashlib.sha256(SECRET_PASSWORD.encode()).hexdigest():
            session['authenticated'] = True
            logger.info("管理员已登录审核界面")
            return redirect(url_for('review'))

    if not session.get('authenticated', False):
        return render_template('review_login.html')

    pending_idioms = load_idioms(PENDING_IDIOM_FILE_PATH)
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

    pending_idioms = load_idioms(PENDING_IDIOM_FILE_PATH)
    current_idioms = load_idioms(IDIOM_FILE_PATH)

    if action == 'approve':
        for idiom in pending_idioms:
            if idiom['word'] == word:
                current_idioms.append(idiom)
                pending_idioms.remove(idiom)
                save_idioms(current_idioms, IDIOM_FILE_PATH)
                save_idioms(pending_idioms, PENDING_IDIOM_FILE_PATH)
                logger.info(f"成语 '{word}' 已通过审核并添加到词库")
                break
    elif action == 'reject':
        original_length = len(pending_idioms)
        pending_idioms = [idiom for idiom in pending_idioms if idiom['word'] != word]
        if len(pending_idioms) < original_length:
            save_idioms(pending_idioms, PENDING_IDIOM_FILE_PATH)
            logger.info(f"成语 '{word}' 已被拒绝")
        else:
            logger.warning(f"尝试拒绝不存在的成语: {word}")

    return redirect(url_for('review'))

if __name__ == '__main__':
    # 仅在非生产环境中启用调试模式
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8666)), debug=debug_mode)
