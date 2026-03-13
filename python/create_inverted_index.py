import sqlite3

DB_PATH = 'idioms.db'

def init_inverted_index():
    """初始化倒排索引表"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 创建倒排索引表
    c.execute('''CREATE TABLE IF NOT EXISTS inverted_index
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  pinyin_element TEXT,
                  idiom_word TEXT,
                  position INTEGER,
                  element_type TEXT, -- 'initial' 或 'final'
                  FOREIGN KEY (idiom_word) REFERENCES idioms(word))''')
    
    # 创建索引
    c.execute('CREATE INDEX IF NOT EXISTS idx_pinyin_element ON inverted_index(pinyin_element)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_idiom_word ON inverted_index(idiom_word)')
    
    conn.commit()
    conn.close()

def get_initials_and_finals(pinyin):
    """获取拼音的声母和韵母"""
    # 预定义声母列表
    INITIALS_LIST = ["zh", "ch", "sh", "b", "p", "m", "f", "d", "t", "n", "l", "g", "k", "h", "j", "q", "x", "r", "z", "c", "s", "y", "w"]
    
    # 查找声母
    initial = ''
    # 先检查双字符声母
    if len(pinyin) >= 2:
        two_char = pinyin[:2]
        if two_char in INITIALS_LIST:
            initial = two_char
    
    # 如果没有找到双字符声母，检查单字符声母
    if not initial and len(pinyin) >= 1:
        one_char = pinyin[:1]
        if one_char in INITIALS_LIST:
            initial = one_char
    
    # 提取韵母
    final = pinyin[len(initial):]
    return initial, final

def build_inverted_index():
    """构建倒排索引"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 清空现有索引
    c.execute('DELETE FROM inverted_index')
    
    # 获取所有成语
    c.execute('SELECT word, pinyin_r FROM idioms')
    idioms = c.fetchall()
    
    total = len(idioms)
    count = 0
    
    for idiom in idioms:
        word = idiom[0]
        pinyin_r = idiom[1]
        pinyin_list = pinyin_r.split()
        
        # 处理每个字的拼音
        for i, pinyin in enumerate(pinyin_list):
            if i >= 4:  # 只处理前4个字
                break
            
            # 获取声母和韵母
            initial, final = get_initials_and_finals(pinyin)
            
            # 存储声母
            if initial:
                c.execute('''INSERT INTO inverted_index 
                           (pinyin_element, idiom_word, position, element_type)
                           VALUES (?, ?, ?, ?)''',
                          (initial, word, i, 'initial'))
            
            # 存储韵母
            if final:
                c.execute('''INSERT INTO inverted_index 
                           (pinyin_element, idiom_word, position, element_type)
                           VALUES (?, ?, ?, ?)''',
                          (final, word, i, 'final'))
        
        count += 1
        if count % 1000 == 0:
            print(f"已处理 {count}/{total} 个成语")
    
    conn.commit()
    conn.close()
    print(f"倒排索引构建完成，共处理 {total} 个成语")

def check_inverted_index():
    """检查倒排索引"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 检查索引数量
    c.execute('SELECT COUNT(*) FROM inverted_index')
    index_count = c.fetchone()[0]
    print(f"倒排索引总数: {index_count}")
    
    # 检查示例索引
    c.execute('SELECT * FROM inverted_index WHERE pinyin_element = "a" LIMIT 5')
    sample_indexes = c.fetchall()
    print("示例索引:")
    for index in sample_indexes:
        print(f"  元素: {index[1]}, 成语: {index[2]}, 位置: {index[3]}, 类型: {index[4]}")
    
    conn.close()

if __name__ == '__main__':
    print("初始化倒排索引表...")
    init_inverted_index()
    print("构建倒排索引...")
    build_inverted_index()
    print("检查倒排索引...")
    check_inverted_index()
    print("倒排索引构建完成!")
