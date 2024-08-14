import sqlite3
import logging
from config import DB_PATH

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        try:
            self.conn = sqlite3.connect(DB_PATH)
            self.create_tables()
            logger.info("Database connection established.")
        except sqlite3.Error as e:
            logger.error(f"Error connecting to the database: {e}")
            raise

    def create_tables(self):
        """Create the necessary tables if they do not exist."""
        try:
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
            logger.info("Database tables created or verified successfully.")
        except sqlite3.Error as e:
            logger.error(f"Error creating tables in the database: {e}")
            raise

    def add_target(self, target: str):
        """Add a new target to the database."""
        try:
            with self.conn:
                self.conn.execute("INSERT OR IGNORE INTO targets (target) VALUES (?)", (target,))
                logger.info(f"Target {target} added to the database.")
        except sqlite3.Error as e:
            logger.error(f"Error adding target to database: {e}")

    def update_results(self, target: str, type: str, result: str):
        """Update the scan results for a given target."""
        try:
            with self.conn:
                target_id = self.conn.execute("SELECT id FROM targets WHERE target = ?", (target,)).fetchone()
                if target_id:
                    self.conn.execute("INSERT INTO results (target_id, type, result) VALUES (?, ?, ?)", (target_id[0], type, result))
                    logger.info(f"Results updated for target {target}.")
                else:
                    logger.warning(f"Target {target} not found in the database.")
        except sqlite3.Error as e:
            logger.error(f"Error updating results in database: {e}")
