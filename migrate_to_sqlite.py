import sqlite3
import json
import os

# 数据库文件路径
DB_PATH = 'idioms.db'
# 成语数据文件路径
IDIOM_FILE_PATH = 'data/idiom.json'
PENDING_IDIOM_FILE_PATH = 'data/pending_idiom.json'

def init_db():
    """初始化数据库"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 创建成语表
    c.execute('''CREATE TABLE IF NOT EXISTS idioms
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  word TEXT UNIQUE,
                  pinyin TEXT,
                  pinyin_r TEXT,
                  derivation TEXT,
                  example TEXT,
                  explanation TEXT,
                  abbreviation TEXT,
                  first TEXT,
                  last TEXT,
                  weight INTEGER DEFAULT 0)''')
    
    # 创建待审核成语表
    c.execute('''CREATE TABLE IF NOT EXISTS pending_idioms
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  word TEXT UNIQUE,
                  pinyin_r TEXT,
                  weight INTEGER DEFAULT 0)''')
    
    # 创建索引
    c.execute('CREATE INDEX IF NOT EXISTS idx_word ON idioms(word)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_pinyin_r ON idioms(pinyin_r)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_first ON idioms(first)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_last ON idioms(last)')
    
    conn.commit()
    conn.close()

def load_idioms_from_json(file_path):
    """从JSON文件加载成语数据"""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            idioms = json.load(file)
    else:
        idioms = []
    return idioms

def migrate_idioms():
    """迁移成语数据到数据库"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 迁移正式成语
    idioms = load_idioms_from_json(IDIOM_FILE_PATH)
    for idiom in idioms:
        try:
            c.execute('''INSERT OR IGNORE INTO idioms 
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
        except Exception as e:
            print(f"Error inserting idiom {idiom.get('word', '')}: {e}")
    
    # 迁移待审核成语
    pending_idioms = load_idioms_from_json(PENDING_IDIOM_FILE_PATH)
    for idiom in pending_idioms:
        try:
            c.execute('''INSERT OR IGNORE INTO pending_idioms 
                       (word, pinyin_r, weight)
                       VALUES (?, ?, ?)''',
                      (idiom.get('word', ''),
                       idiom.get('pinyin_r', ''),
                       idiom.get('weight', 0)))
        except Exception as e:
            print(f"Error inserting pending idiom {idiom.get('word', '')}: {e}")
    
    conn.commit()
    conn.close()
    print(f"Migrated {len(idioms)} idioms and {len(pending_idioms)} pending idioms to database")

def check_migration():
    """检查迁移结果"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 检查成语数量
    c.execute('SELECT COUNT(*) FROM idioms')
    idiom_count = c.fetchone()[0]
    print(f"Total idioms in database: {idiom_count}")
    
    # 检查待审核成语数量
    c.execute('SELECT COUNT(*) FROM pending_idioms')
    pending_count = c.fetchone()[0]
    print(f"Total pending idioms in database: {pending_count}")
    
    # 检查示例数据
    c.execute('SELECT word, pinyin_r FROM idioms LIMIT 5')
    sample_idioms = c.fetchall()
    print("Sample idioms:")
    for idiom in sample_idioms:
        print(f"  {idiom[0]}: {idiom[1]}")
    
    conn.close()

if __name__ == '__main__':
    print("Initializing database...")
    init_db()
    print("Migrating idioms...")
    migrate_idioms()
    print("Checking migration...")
    check_migration()
    print("Migration completed!")
