import logging
from uvicorn.logging import DefaultFormatter

import sqlite3
from pathlib import Path

#logging.basicConfig(
#    level=logging.INFO,
#    format="%(levelname)-9s %(name)s:%(funcName)s:%(lineno)d | %(message)s"
#)

handler = logging.StreamHandler()
handler.setFormatter(DefaultFormatter(
    fmt="%(levelprefix)-9s | %(funcName)s:%(lineno)d | %(message)s",
    use_colors=True
))

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

BASE_DIR = Path.cwd()
DB_PATH = BASE_DIR / "app/data/mht.db"
CREATE_TABLES_PATH = BASE_DIR / "app/db/create_tables.sql"
FILL_TABLES_PATH = BASE_DIR / "app/db/fill_tables.sql"

logging.info(f"Base Dir : {BASE_DIR}")
logging.info(f"DB PATH : {DB_PATH}")
logging.info(f"CREATE_TABLE_PATH : {CREATE_TABLES_PATH}")
logging.info(f"FILL_TABLES_PATH : {FILL_TABLES_PATH}")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db() -> None:
    conn = get_connection()
    try:
        with open(CREATE_TABLES_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
            logging.info(f"mth.db created")

        # Remplit les tables que si la table actress est vide
        count = conn.execute("SELECT COUNT(*) FROM actress").fetchone()[0]

        if count == 0:
            with open(FILL_TABLES_PATH , "r", encoding="utf-8") as f:
                conn.executescript(f.read())
                logging.info(f"mth.db filled")

        conn.commit()
        
    finally:
        conn.close()