from db import get_db_connection

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
    import re
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
    """解析用户输入的拼音条件"""
    import re
    return re.split(r'[^a-zA-ZüÜ]+', input_str)

# 搜索函数
def search_idioms(include_initials, include_finals, exclude_initials, exclude_finals,
                  position_include_conditions, position_exclude_conditions):
    """搜索符合条件的成语
    
    Args:
        include_initials (set): 包含的声母集合
        include_finals (set): 包含的韵母集合
        exclude_initials (set): 排除的声母集合
        exclude_finals (set): 排除的韵母集合
        position_include_conditions (list): 位置包含条件列表
        position_exclude_conditions (list): 位置排除条件列表
        
    Returns:
        list: 符合条件的成语列表
    """
    conn = get_db_connection()
    c = conn.cursor()
    
    # 使用倒排索引快速过滤成语
    # 构建包含条件的查询
    included_words = set()
    
    # 如果有包含条件，使用倒排索引过滤
    if include_initials or include_finals:
        # 构建查询条件
        conditions = []
        params = []
        
        # 添加声母条件
        for initial in include_initials:
            conditions.append('(pinyin_element = ? AND element_type = "initial")')
            params.append(initial)
        
        # 添加韵母条件
        for final in include_finals:
            conditions.append('(pinyin_element = ? AND element_type = "final")')
            params.append(final)
        
        if conditions:
            # 查询包含所有指定拼音元素的成语
            query = f"""
            SELECT idiom_word, COUNT(DISTINCT pinyin_element) as match_count
            FROM inverted_index
            WHERE {' OR '.join(conditions)}
            GROUP BY idiom_word
            HAVING match_count = ?
            """
            params.append(len(include_initials) + len(include_finals))
            
            c.execute(query, params)
            results = c.fetchall()
            included_words = {row['idiom_word'] for row in results}
    else:
        # 如果没有包含条件，获取所有成语
        c.execute('SELECT word FROM idioms')
        results = c.fetchall()
        included_words = {row['word'] for row in results}
    
    # 排除指定的拼音元素
    if exclude_initials or exclude_finals:
        # 构建排除条件
        exclude_conditions = []
        exclude_params = []
        
        # 添加排除的声母
        for initial in exclude_initials:
            exclude_conditions.append('(pinyin_element = ? AND element_type = "initial")')
            exclude_params.append(initial)
        
        # 添加排除的韵母
        for final in exclude_finals:
            exclude_conditions.append('(pinyin_element = ? AND element_type = "final")')
            exclude_params.append(final)
        
        if exclude_conditions:
            # 查询包含排除拼音元素的成语
            exclude_query = f"""
            SELECT DISTINCT idiom_word
            FROM inverted_index
            WHERE {' OR '.join(exclude_conditions)}
            """
            c.execute(exclude_query, exclude_params)
            exclude_results = c.fetchall()
            excluded_words = {row['idiom_word'] for row in exclude_results}
            
            # 从包含列表中移除排除的成语
            included_words = included_words - excluded_words
    
    # 获取候选成语的详细信息
    if included_words:
        placeholders = ','.join(['?'] * len(included_words))
        c.execute(f"SELECT word, pinyin_r, weight FROM idioms WHERE word IN ({placeholders}) ORDER BY weight DESC", list(included_words))
        candidate_idioms = c.fetchall()
    else:
        candidate_idioms = []
    
    conn.close()
    
    # 进一步过滤位置条件
    result_idioms = []
    for idiom in candidate_idioms:
        word = idiom['word']
        pinyin_r = idiom['pinyin_r']
        weight = idiom['weight']
        
        if len(word) != 4 or len(pinyin_r.split()) != 4:
            continue

        pinyin_list = pinyin_r.split()
        initial_matches = [get_initials_and_finals(pinyin)[0] for pinyin in pinyin_list]
        final_matches = [get_initials_and_finals(pinyin)[1] for pinyin in pinyin_list]

        def matches_conditions(initials, finals, include_cond, exclude_cond):
            include_initials, include_finals = include_cond
            exclude_initials, exclude_finals = exclude_cond

            return all(x in initials for x in include_initials) and \
                   all(x in finals for x in include_finals) and \
                   not any(x in initials for x in exclude_initials) and \
                   not any(x in finals for x in exclude_finals)

        # 检查位置条件
        satisfies_position_conditions = True
        for i in range(4):
            if not matches_conditions([initial_matches[i]], [final_matches[i]], position_include_conditions[i], position_exclude_conditions[i]):
                satisfies_position_conditions = False
                break

        if satisfies_position_conditions:
            result_idioms.append({'word': word, 'pinyin': pinyin_r, 'weight': weight})

    # 按权重排序
    result_idioms.sort(key=lambda x: x['weight'], reverse=True)
    return result_idioms
