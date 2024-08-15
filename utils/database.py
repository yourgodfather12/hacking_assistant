import sqlite3
import logging
import os
from config import DB_PATH

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        try:
            # Ensure the directory for the database exists
            db_dir = os.path.dirname(DB_PATH)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir)

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
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        target TEXT UNIQUE NOT NULL
                    )
                """)
                self.conn.execute("""
                    CREATE TABLE IF NOT EXISTS results (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        target_id INTEGER NOT NULL,
                        type TEXT NOT NULL,
                        result TEXT NOT NULL,
                        FOREIGN KEY (target_id) REFERENCES targets(id) ON DELETE CASCADE
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
                cursor = self.conn.execute("INSERT OR IGNORE INTO targets (target) VALUES (?)", (target,))
                if cursor.rowcount > 0:
                    logger.info(f"Target {target} added to the database.")
                else:
                    logger.info(f"Target {target} already exists in the database.")
        except sqlite3.Error as e:
            logger.error(f"Error adding target to database: {e}")
            raise

    def update_results(self, target: str, scan_type: str, result: str):
        """Update the scan results for a given target."""
        try:
            with self.conn:
                target_id = self.conn.execute("SELECT id FROM targets WHERE target = ?", (target,)).fetchone()
                if target_id:
                    self.conn.execute(
                        "INSERT INTO results (target_id, type, result) VALUES (?, ?, ?)",
                        (target_id[0], scan_type, result)
                    )
                    logger.info(f"Results updated for target {target}.")
                else:
                    logger.warning(f"Target {target} not found in the database.")
        except sqlite3.Error as e:
            logger.error(f"Error updating results in database: {e}")
            raise

    def fetch_all_targets(self):
        """Fetch all targets from the database."""
        try:
            with self.conn:
                targets = self.conn.execute("SELECT target FROM targets").fetchall()
                return [target[0] for target in targets]
        except sqlite3.Error as e:
            logger.error(f"Error fetching targets from database: {e}")
            raise

    def fetch_results_by_target(self, target: str):
        """Fetch all scan results for a given target."""
        try:
            with self.conn:
                target_id = self.conn.execute("SELECT id FROM targets WHERE target = ?", (target,)).fetchone()
                if target_id:
                    results = self.conn.execute(
                        "SELECT type, result FROM results WHERE target_id = ?", (target_id[0],)
                    ).fetchall()
                    return [{"type": row[0], "result": row[1]} for row in results]
                else:
                    logger.warning(f"No results found for target {target}.")
                    return []
        except sqlite3.Error as e:
            logger.error(f"Error fetching results from database: {e}")
            raise

    def close(self):
        """Close the database connection."""
        try:
            if self.conn:
                self.conn.close()
                logger.info("Database connection closed.")
        except sqlite3.Error as e:
            logger.error(f"Error closing the database connection: {e}")
            raise
