const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const config = require('../config/config');

// 确保数据目录存在
const fs = require('fs');
const dataDir = path.dirname(config.DB_PATH);
if (!fs.existsSync(dataDir)) {
  fs.mkdirSync(dataDir, { recursive: true });
}

// 数据库连接
let db;

/**
 * 获取数据库连接
 * @returns {sqlite3.Database} 数据库连接对象
 */
function getDbConnection() {
  if (!db) {
    db = new sqlite3.Database(config.DB_PATH, (err) => {
      if (err) {
        console.error('Error opening database:', err.message);
      } else {
        console.log('Connected to the SQLite database.');
        // 初始化数据库表
        initDatabase();
      }
    });
  }
  return db;
}

/**
 * 初始化数据库表
 */
function initDatabase() {
  const db = getDbConnection();
  
  // 创建成语表
  db.run(`
    CREATE TABLE IF NOT EXISTS idioms (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      word TEXT UNIQUE NOT NULL,
      pinyin TEXT,
      pinyin_r TEXT NOT NULL,
      derivation TEXT,
      example TEXT,
      explanation TEXT,
      abbreviation TEXT,
      first TEXT,
      last TEXT,
      weight INTEGER DEFAULT 0
    )
  `);
  
  // 创建待审核成语表
  db.run(`
    CREATE TABLE IF NOT EXISTS pending_idioms (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      word TEXT UNIQUE NOT NULL,
      pinyin_r TEXT NOT NULL,
      weight INTEGER DEFAULT 0
    )
  `);
  
  // 创建倒排索引表
  db.run(`
    CREATE TABLE IF NOT EXISTS inverted_index (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      idiom_word TEXT NOT NULL,
      pinyin_element TEXT NOT NULL,
      element_type TEXT NOT NULL,
      position INTEGER,
      FOREIGN KEY (idiom_word) REFERENCES idioms (word)
    )
  `);
  
  // 创建索引
  db.run('CREATE INDEX IF NOT EXISTS idx_inverted_index_element ON inverted_index (pinyin_element, element_type)');
  db.run('CREATE INDEX IF NOT EXISTS idx_inverted_index_idiom ON inverted_index (idiom_word)');
}

/**
 * 关闭数据库连接
 */
function closeDbConnection() {
  if (db) {
    db.close((err) => {
      if (err) {
        console.error('Error closing database:', err.message);
      } else {
        console.log('Database connection closed.');
        db = null;
      }
    });
  }
}

module.exports = {
  getDbConnection,
  closeDbConnection,
  initDatabase
};