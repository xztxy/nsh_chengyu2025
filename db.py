import sqlite3
from config import Config

def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(Config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def load_idioms():
    """从数据库加载成语数据"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM idioms')
    idioms = [dict(row) for row in c.fetchall()]
    conn.close()
    return idioms

def load_pending_idioms():
    """从数据库加载待审核成语数据"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM pending_idioms')
    idioms = [dict(row) for row in c.fetchall()]
    conn.close()
    return idioms

def save_idiom(idiom):
    """保存成语到数据库"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO idioms 
               (word, pinyin, pinyin_r, derivation, example, explanation, abbreviation, first, last, weight)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (idiom.get('word', ''),
               idiom.get('pinyin', ''),
               idiom.get('pinyin_r', ''),
               idiom.get('derivation', ''),
               idiom.get('example', ''),
               idiom.get('explanation', ''),
               idiom.get('abbreviation', ''),
               idiom.get('first', ''),
               idiom.get('last', ''),
               idiom.get('weight', 0)))
    conn.commit()
    conn.close()

def save_pending_idiom(idiom):
    """保存待审核成语到数据库"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO pending_idioms 
               (word, pinyin_r, weight)
               VALUES (?, ?, ?)''',
              (idiom.get('word', ''),
               idiom.get('pinyin_r', ''),
               idiom.get('weight', 0)))
    conn.commit()
    conn.close()

def update_idiom_weight(word, weight):
    """更新成语权重"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('UPDATE idioms SET weight = ? WHERE word = ?', (weight, word))
    conn.commit()
    conn.close()

def delete_pending_idiom(word):
    """删除待审核成语"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM pending_idioms WHERE word = ?', (word,))
    conn.commit()
    conn.close()

def check_idiom_exists(word):
    """检查成语是否存在"""
    conn = get_db_connection()
    c = conn.cursor()
    
    # 检查正式成语
    c.execute('SELECT word FROM idioms WHERE word = ?', (word,))
    if c.fetchone():
        conn.close()
        return True
    
    # 检查待审核成语
    c.execute('SELECT word FROM pending_idioms WHERE word = ?', (word,))
    if c.fetchone():
        conn.close()
        return True
    
    conn.close()
    return False

def get_idiom_detail(word):
    """获取成语详情"""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM idioms WHERE word = ?', (word,))
    idiom = c.fetchone()
    conn.close()
    return dict(idiom) if idiom else None