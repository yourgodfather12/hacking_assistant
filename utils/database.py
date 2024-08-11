import sqlite3
from config import DB_PATH
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS targets (
                    id INTEGER PRIMARY KEY,
                    target TEXT UNIQUE
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY,
                    target_id INTEGER,
                    type TEXT,
                    result TEXT,
                    FOREIGN KEY (target_id) REFERENCES targets(id)
                )
            """)

    def add_target(self, target):
        try:
            with self.conn:
                self.conn.execute("INSERT OR IGNORE INTO targets (target) VALUES (?)", (target,))
        except sqlite3.Error as e:
            logger.error(f"Error adding target to database: {e}")

    def update_results(self, target, type, result):
        try:
            with self.conn:
                target_id = self.conn.execute("SELECT id FROM targets WHERE target = ?", (target,)).fetchone()[0]
                self.conn.execute("INSERT INTO results (target_id, type, result) VALUES (?, ?, ?)", (target_id, type, result))
        except sqlite3.Error as e:
            logger.error(f"Error updating results in database: {e}")
