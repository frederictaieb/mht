import sqlite3
from pathlib import Path

#logging.basicConfig(
#    level=logging.INFO,
#    format="%(levelname)-9s %(name)s:%(funcName)s:%(lineno)d | %(message)s"
#)

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./app/data/mht.db"


#Base = declarative_base()

#BASE_DIR = Path.cwd()
#DB_PATH = BASE_DIR / "app/data/mht.db"
#CREATE_TABLES_PATH = BASE_DIR / "app/db/create_tables.sql"
#FILL_TABLES_PATH = BASE_DIR / "app/db/fill_tables.sql"

#logging.info(f"Base Dir : {BASE_DIR}")
#logging.info(f"DB PATH : {DB_PATH}")
#logging.info(f"CREATE_TABLE_PATH : {CREATE_TABLES_PATH}")
#logging.info(f"FILL_TABLES_PATH : {FILL_TABLES_PATH}")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

#def get_connection() -> sqlite3.Connection:
#    conn = sqlite3.connect(DB_PATH)
#    conn.row_factory = sqlite3.Row
#    conn.execute("PRAGMA foreign_keys = ON;")
#    return conn


#def init_db() -> None:
#    conn = get_connection()
#    try:
#        with open(CREATE_TABLES_PATH, "r", encoding="utf-8") as f:
#            conn.executescript(f.read())
#            logging.info(f"mth.db created")

#        # Remplit les tables que si la table actress est vide
#        count = conn.execute("SELECT COUNT(*) FROM actress").fetchone()[0]

#        if count == 0:
#            with open(FILL_TABLES_PATH , "r", encoding="utf-8") as f:
#                conn.executescript(f.read())
#                logging.info(f"mth.db filled")

#        conn.commit()
        
#    finally:
#        conn.close()